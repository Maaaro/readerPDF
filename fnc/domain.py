import os
import threading
from enum import Enum

from fnc.case import Case
from fnc.provider_invoices import find_invoices, is_dir_empty, is_there_any_pdf_files, directory_files, read_pdf_content


class InvoiceSearchMode(Enum):
    FULL = 1
    BY_WORKFLOW_NUMBER = 2


def which_files_to_move(cases: list[Case],
                        mode: InvoiceSearchMode,
                        source: str,
                        target: str,
                        progressbar_callback=None,
                        stop_event: threading.Event = None) -> tuple[dict[str, list[str]], list[str]]:
    files_to_move = {}
    found_invoice_numbers = []

    # ✅ Track matches per case using filePrefix as key instead of Case object
    matches_per_case = {case.filePrefix: 0 for case in cases}

    # ✅ Group cases by their search directory
    cases_by_directory = {}
    for case in cases:
        if mode == InvoiceSearchMode.BY_WORKFLOW_NUMBER:
            directory = os.path.join(source, case.workflowNumber).replace("\\", "/")
        else:
            directory = source

        if directory not in cases_by_directory:
            cases_by_directory[directory] = []
        cases_by_directory[directory].append(case)

    processed_cases = 0

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
            if stop_event and stop_event.is_set():
                break

            full_path = make_source_path(directory, file)
            content = read_pdf_content(full_path)  # ✅ Read once!

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

        processed_cases += len(directory_cases)
        if progressbar_callback:
            progressbar_callback(processed_cases)

    return files_to_move, list(found_invoice_numbers)


# old code
# def which_files_to_move(cases: list[Case],
#                         mode: InvoiceSearchMode,
#                         source: str,
#                         target: str,
#                         progressbar_callback=None,
#                         stop_event: threading.Event = None) -> tuple[dict[str, str], list[str]]:
#     files_to_move = {}
#     found_invoice_numbers = []
#     for index, case in enumerate(cases):
#         if stop_event and stop_event.is_set():
#             break
#         if mode == InvoiceSearchMode.BY_WORKFLOW_NUMBER:
#             modified_source = os.path.join(source, case.workflowNumber).replace("\\", "/")
#         else:
#             modified_source = source
#         found_invoices = find_invoices(modified_source, invoiceNumber=case.providerInvoiceNumber)
#         for i, invoice_file in enumerate(found_invoices):
#             if len(found_invoices) > 1:
#                 suffix = '-' + str(i + 1)
#             else:
#                 suffix = ''
#             source_path = make_source_path(modified_source, invoice_file)
#             target_path = make_source_path(target, (case.filePrefix + suffix + '.pdf'))
#             if source_path not in files_to_move:
#                 files_to_move[source_path] = []
#             files_to_move[source_path].append(target_path)
#             found_invoice_numbers.append(case.providerInvoiceNumber)
#         if progressbar_callback:
#             progressbar_callback(index + 1)
#
#     return files_to_move, (list(found_invoice_numbers))


def make_source_path(source: str, file: str) -> str:
    return os.path.join(source, file).replace("\\", "/")
