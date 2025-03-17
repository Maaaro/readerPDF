from pytest import raises

from fnc.provider_invoices import find_invoices

def test_empty_provider_invoice_directory_is_invalid():
    with raises(Exception) as exception_info:
        find_invoices('fixture/emptyDir', 'numer faktury')
    assert str(exception_info.value) == 'Provider invoice directory is empty.'

def test_file_containing_invoice_number_is_returned():
    found_invoices = find_invoices('fixture/invoices',
                                   '100156909563/RA/2024')
    assert found_invoices == ['100156909563.pdf']
