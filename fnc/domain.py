import os
import threading
from enum import Enum
from typing import Any

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
    files_to_move = {}
    found_invoice_numbers = []

    # Track matches per case using filePrefix as key instead of Case object
    matches_per_case = {case.filePrefix: 0 for case in cases}

    cases_by_directory = get_search_directories(cases, mode, source)

    processed_pdfs = 0

    # For each directory, read each PDF once and check all invoice numbers
    for directory, directory_cases in cases_by_directory.items():
        if stop_event and stop_event.is_set():
            break

        is_directory_raise_exception(directory)

        # Read each PDF once
        for file in directory_files(directory):
            if stop_event and stop_event.is_set():
                break

            full_path = make_source_path(directory, file)
            content = read_pdf_content(full_path)

            # Check all invoice numbers from cases in this directory
            for case in directory_cases:
                if case.providerInvoiceNumber in content:
                    invoice_found_in_content(case, files_to_move, found_invoice_numbers, full_path, matches_per_case,
                                             target)

            processed_pdfs += 1
            if progressbar_callback:
                progressbar_callback(processed_pdfs)

    return files_to_move, list(found_invoice_numbers)


def invoice_found_in_content(case: Case, files_to_move: dict[Any, Any], found_invoice_numbers: list[Any],
                             full_path: str, matches_per_case: dict[str, int], target: str):
    matches_per_case[case.filePrefix] += 1
    match_count = matches_per_case[case.filePrefix]

    target_path = building_target_path(case, match_count, target)

    if full_path not in files_to_move:
        files_to_move[full_path] = []

    files_to_move[full_path].append(target_path)
    found_invoice_numbers.append(case.providerInvoiceNumber)


def building_target_path(case: Case, match_count: int, target: str) -> str:
    suffix = '-' + str(match_count) if match_count > 1 else ''
    target_path = make_source_path(target, case.filePrefix + suffix + '.pdf')
    return target_path


def is_directory_raise_exception(directory: str):
    if is_dir_empty(directory):
        raise Exception(f'Provider invoice directory is empty.')
    if not is_there_any_pdf_files(directory):
        raise Exception(f'Provider invoice directory does not contain invoices.')


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
