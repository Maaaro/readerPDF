import os
from enum import Enum

from fnc.case import Case
from fnc.provider_invoices import find_invoices

class SearchMode(Enum):
    FULL = 1
    BY_WORKFLOW_NUMBER = 2

def which_files_to_move(cases: list[Case],
                        mode: SearchMode,
                        source: str,
                        target: str) -> dict[str, str]:
    files_to_move = {}
    for case in cases:
        found_invoices = find_invoices(source, invoiceNumber=case.providerInvoiceNumber)
        if len(found_invoices) == 0:
            pass
        else:
            for index, invoice_file in enumerate(found_invoices):
                if len(found_invoices) > 1:
                    suffix = '-' + str(index + 1)
                else:
                    suffix = ''

                source_path = make_source_path(source, invoice_file)
                target_path = os.path.join(target, case.filePrefix + suffix + '.pdf')

                files_to_move[source_path] = target_path

    return files_to_move

def make_source_path(source: str, file: str):
    return os.path.join(source, file).replace('\\', '/')

