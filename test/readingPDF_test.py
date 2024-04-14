import pytest
import glob


def listOfLinks(source):
    source = "C:/Users/mrowk/Downloads/FAKTURY/*.pdf"
    try:
        sourceList = glob.glob(source)
        print("Lista zrodel: ", sourceList)
    except:
        print("Brak plików PDF w katalogu!")

def test1():
    assert listOfLinks("aaa") is str

def test2():
    assert 1 == 2
