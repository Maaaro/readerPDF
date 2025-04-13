from fnc.case import Case

from fnc.domain import which_files_to_move, InvoiceSearchMode
from test.project_path import project_path

def test_for_single_invoice_saves_invoice_only_with_case_prefix():
    files_to_move = which_files_to_move(
        cases=[Case('eIC155687424', '420', None)],
        mode=InvoiceSearchMode.FULL,
        source=project_path('domain/fixture/single_invoice'),
        target='output/')
    assert files_to_move == {
        project_path('domain/fixture/single_invoice/eic_155687424.pdf'): 'output/420.pdf'
    }

def test_for_multiple_invoices_saves_file_with_case_prefix_and_suffix():
    files_to_move = which_files_to_move(
        cases=[Case('eIC155687424', '42', None)],
        mode=InvoiceSearchMode.FULL,
        source=project_path('domain/fixture/multiple_invoices'),
        target='output/')
    assert files_to_move == {
        project_path('domain/fixture/multiple_invoices/eic_155687424.pdf'): 'output/42-1.pdf',
        project_path('domain/fixture/multiple_invoices/eic_155687424_copy.pdf'): 'output/42-2.pdf',
    }

def test_search_in_subfolder_with_name_of_workflow_number():
    files_to_move = which_files_to_move(
        cases=[Case('eIC155687424', '420', "wf1")],
        mode=InvoiceSearchMode.BY_WORKFLOW_NUMBER,
        source=project_path('domain/fixture/with_wf_number'),
        target='output/')
    assert files_to_move == {
        project_path('domain/fixture/with_wf_number/wf1/eic_155687424.pdf'): 'output/420.pdf'
    }
