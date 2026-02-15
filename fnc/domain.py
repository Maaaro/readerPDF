import os
import threading
from enum import Enum

from fnc.case import Case
from fnc.provider_invoices import find_invoices


class InvoiceSearchMode(Enum):
    FULL = 1
    BY_WORKFLOW_NUMBER = 2


def which_files_to_move(cases: list[Case],
                        mode: InvoiceSearchMode,
                        source: str,
                        target: str,
                        progressbar_callback=None,
                        stop_event: threading.Event = None) -> tuple[dict[str, str], list[str]]:
    files_to_move = {}
    found_invoice_numbers = []
    for index, case in enumerate(cases):
        if stop_event and stop_event.is_set():
            break
        if mode == InvoiceSearchMode.BY_WORKFLOW_NUMBER:
            modified_source = os.path.join(source, case.workflowNumber).replace("\\", "/")
        else:
            modified_source = source
        found_invoices = find_invoices(modified_source, invoiceNumber=case.providerInvoiceNumber)
        for i, invoice_file in enumerate(found_invoices):
            if len(found_invoices) > 1:
                suffix = '-' + str(i + 1)
            else:
                suffix = ''
            source_path = make_source_path(modified_source, invoice_file)
            target_path = make_source_path(target, (case.filePrefix + suffix + '.pdf'))
            if source_path not in files_to_move:
                files_to_move[source_path] = []
            files_to_move[source_path].append(target_path)
            found_invoice_numbers.append(case.providerInvoiceNumber)
        if progressbar_callback:
            progressbar_callback(index + 1)

    return files_to_move, (list(found_invoice_numbers))


def make_source_path(source: str, file: str) -> str:
    return os.path.join(source, file).replace("\\", "/")
