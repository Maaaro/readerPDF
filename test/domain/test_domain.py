from fnc.case import Case

from fnc.domain import which_files_to_move, SearchMode

def test_for_single_invoice_saves_invoice_only_with_case_prefix():
    files_to_move = which_files_to_move(
        cases=[Case('eIC155687424', '420', None)],
        mode=SearchMode.FULL,
        source='fixture/single_invoice',
        target='output/')
    assert files_to_move == {
        'fixture/single_invoice/eic_155687424.pdf': 'output/420.pdf'
    }

def test_for_multiple_invoices_saves_file_with_case_prefix_and_suffix():
    files_to_move = which_files_to_move(
        cases=[Case('eIC155687424', '42', None)],
        mode=SearchMode.FULL,
        source='fixture/multiple_invoices',
        target='output/')
    assert files_to_move == {
        'fixture/multiple_invoices/eic_155687424.pdf': 'output/42-1.pdf',
        'fixture/multiple_invoices/eic_155687424_copy.pdf': 'output/42-2.pdf',
    }

def test_search_by_directory():
    pass
