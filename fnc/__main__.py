import threading

from fnc.case import read_input_cases, update_excel_df, Case
from fnc.domain import which_files_to_move, InvoiceSearchMode, get_search_directories
from fnc.provider_invoices import is_there_any_pdf_files, is_dir_empty, directory_files
from fnc.view.values import SearchRequest, LimitedSearch
from fnc.view.view import View
from test.copy_files.move_files import copy_found_invoices_to_target_dir


def count_total_pdfs(cases: list[Case], mode: InvoiceSearchMode, source: str) -> int:
    cases_by_directory = get_search_directories(cases, mode, source)

    total_pdfs = 0
    for directory in cases_by_directory.keys():
        if not is_dir_empty(directory) and is_there_any_pdf_files(directory):
            total_pdfs += len(directory_files(directory))

    return total_pdfs


def zostalem_powiadomiony(request: SearchRequest):
    print("----")
    print("Jestem kodem z maina, ktory dostal info z widoku, a widok dostał info z gui")
    print("Sciezka: " + request.invoice_folder)
    print("Docelowy: " + request.target_folder)
    print("Ścieżka excela: " + request.excel_path)
    print("Syrcz mołd: " + str(request.limited_search))

    list_of_cases, excel_df = read_input_cases(request.excel_path)

    if request.limited_search == LimitedSearch.LIMITED:
        mold = InvoiceSearchMode.BY_WORKFLOW_NUMBER
    else:
        mold = InvoiceSearchMode.FULL

    total_pdfs = count_total_pdfs(list_of_cases, mold, request.invoice_folder)

    stop_event = threading.Event()

    def on_close():
        print("🔴 ON_CLOSE CALLED!")
        import traceback
        traceback.print_stack()
        stop_event.set()
        view.close_progressbar_window()

    view.show_progressbar_window(total_pdfs, on_close=on_close)

    def run():
        print("🔵 THREAD STARTED")  # ✅ na samym początku funkcji run
        try:
            files_to_move, invoices_found = which_files_to_move(
                list_of_cases,
                mold,
                request.invoice_folder,
                request.target_folder,
                progressbar_callback=lambda current: view.run_on_main_thread(
                    lambda c=current: view.update_progressbar(c, total_pdfs)),
                stop_event=stop_event
            )
            print("🟢 which_files_to_move FINISHED")

            if stop_event.is_set():
                print("🟠 STOP EVENT WAS SET")
                return

            copy_found_invoices_to_target_dir(files_to_move)
            update_excel_df(excel_df, invoices_found, request.excel_path)
            view.run_on_main_thread(view.close_progressbar_window)
            view.run_on_main_thread(view.finished)

            print("Program ma problem z wyszukiwaniem. przykład. Nr fv = 1234 - nie znajdzie. nr fv = '1234' - znajdzie")

            print(files_to_move)
            print(invoices_found)

        except Exception as e:
            print(f"🔴 ERROR IN THREAD: {e}")
            import traceback
            traceback.print_exc()

    thread = threading.Thread(target=run)
    print("🔵 STARTING THREAD")
    thread.start()
    print("🔵 THREAD STARTED (non-blocking)")


if __name__ == '__main__':
    view = View(zostalem_powiadomiony)
    view.show_window()
