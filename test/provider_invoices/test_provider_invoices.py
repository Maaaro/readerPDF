import os

from pytest import raises

from fnc.case import Case
from fnc.domain import which_files_to_move, InvoiceSearchMode
from test.project_path import project_path


def test_directory_without_provider_invoices_is_invalid():
    with raises(Exception) as exception_info:
        path = project_path('provider_invoices/fixture/dir_without_invoices')
        which_files_to_move(
            cases=[Case('numer faktury', 'test', None)],
            mode=InvoiceSearchMode.FULL,
            source=path,
            target='output/')
    assert str(exception_info.value) == 'Provider invoice directory does not contain invoices.'


def test_file_containing_invoice_number_is_returned():
    path = project_path('provider_invoices/fixture/invoices')
    files_to_move, _ = which_files_to_move(
        cases=[Case('100156909563/RA/2024', 'test', None)],
        mode=InvoiceSearchMode.FULL,
        source=path,
        target='output/')
    found_files = [os.path.basename(key) for key in files_to_move.keys()]
    assert found_files == ['100156909563.pdf']


def test_file_containing_invoice_number_in_subfolder():
    path = project_path('provider_invoices/fixture/invoices_in_subfolder/')
    files_to_move, _ = which_files_to_move(
        cases=[Case('PL3654810710', 'test', None)],
        mode=InvoiceSearchMode.FULL,
        source=path,
        target='output/'
    )
    found_files = [os.path.relpath(key, path).replace('\\', '/') for key in files_to_move.keys()]
    assert found_files == ['subfolder1/decathlon-invoice-12300750000756593.pdf']
