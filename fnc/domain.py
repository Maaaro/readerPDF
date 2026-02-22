import os
import threading
from enum import Enum

from fnc.case import Case
from fnc.provider_invoices import is_dir_empty, is_there_any_pdf_files, directory_files, read_pdf_content


class InvoiceSearchMode(Enum):
    FULL = 1
    BY_WORKFLOW_NUMBER = 2


def which_files_to_move(cases: list[Case],
                        mode: InvoiceSearchMode,
                        source: str,
                        target: str,
                        progressbar_callback=None,
                        stop_event: threading.Event = None) -> tuple[dict[str, list[str]], list[str]]:
    print("🔵 which_files_to_move CALLED")
    files_to_move = {}
    found_invoice_numbers = []

    # ✅ Track matches per case using filePrefix as key instead of Case object
    matches_per_case = {case.filePrefix: 0 for case in cases}

    cases_by_directory = get_search_directories(cases, mode, source)

    processed_pdfs = 0

    # ✅ For each directory, read each PDF once and check all invoice numbers
    for directory, directory_cases in cases_by_directory.items():
        if stop_event and stop_event.is_set():
            break

        if is_dir_empty(directory):
            raise Exception(f'Provider invoice directory is empty: {directory}')
        if not is_there_any_pdf_files(directory):
            raise Exception(f'Provider invoice directory does not contain invoices: {directory}')

        # ✅ Read each PDF once
        for file in directory_files(directory):
            print(f"Processing PDF {processed_pdfs + 1}: {file}")

            if stop_event and stop_event.is_set():
                print("STOP EVENT SET!")
                break

            full_path = make_source_path(directory, file)
            content = read_pdf_content(full_path)

            # ✅ Check all invoice numbers from cases in this directory
            for case in directory_cases:


                if case.providerInvoiceNumber in content:
                    matches_per_case[case.filePrefix] += 1
                    match_count = matches_per_case[case.filePrefix]

                    suffix = '-' + str(match_count) if match_count > 1 else ''
                    target_path = make_source_path(target, case.filePrefix + suffix + '.pdf')

                    if full_path not in files_to_move:
                        files_to_move[full_path] = []
                    files_to_move[full_path].append(target_path)
                    found_invoice_numbers.append(case.providerInvoiceNumber)

            processed_pdfs += 1
            print(f"Finished processing, calling callback with {processed_pdfs}")
            if progressbar_callback:
                progressbar_callback(processed_pdfs)

    return files_to_move, list(found_invoice_numbers)


def make_source_path(source: str, file: str) -> str:
    return os.path.join(source, file).replace("\\", "/")


def get_search_directories(cases: list[Case], mode: InvoiceSearchMode, source: str) -> dict[str, list[Case]]:
    cases_by_directory = {}

    for case in cases:
        if mode == InvoiceSearchMode.BY_WORKFLOW_NUMBER:
            directory = os.path.join(source, case.workflowNumber).replace("\\", "/")
        else:
            directory = source

        if directory not in cases_by_directory:
            cases_by_directory[directory] = []
        cases_by_directory[directory].append(case)

    return cases_by_directory
