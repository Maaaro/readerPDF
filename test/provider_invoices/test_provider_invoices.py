from pytest import raises

from fnc.provider_invoices import find_invoices
from test.project_path import project_path


def test_directory_without_provider_invoices_is_invalid():
    with raises(Exception) as exception_info:
        path = project_path('provider_invoices/fixture/dir_without_invoices')
        find_invoices(path, 'numer faktury')
    assert str(exception_info.value) == 'Provider invoice directory does not contain invoices.'

def test_file_containing_invoice_number_is_returned():
    path = project_path('provider_invoices/fixture/invoices')
    found_invoices = find_invoices(path, '100156909563/RA/2024')
    assert found_invoices == [path + "/" + '100156909563.pdf']

def test_file_containing_invoice_number_in_subfolder():
    path = project_path('provider_invoices/fixture/invoices_in_subfolder')
    found_invoices = find_invoices(path, 'PL3654810710')
    assert found_invoices == [path + "/" + 'subfolder1/decathlon-invoice-12300750000756593.pdf']