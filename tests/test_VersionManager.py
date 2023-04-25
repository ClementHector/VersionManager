import pytest
from version_manager import VersionManager

def test_init():
    version = VersionManager()
    assert version.release() == "0.0.1"

    version = VersionManager("1")
    assert version.release() == "1.0.0"

    version = VersionManager("1.2")
    assert version.release() == "1.2.0"

    version = VersionManager("1.2.3")
    assert version.release() == "1.2.3"

    with pytest.raises(Exception) as excinfo:
        VersionManager("invalid")
    assert str(excinfo.value) == "Error occurred while parsing version!"

def test_major():
    version = VersionManager("1.2.3")
    version.major()
    assert version.release() == "2.0.0"

def test_minor():
    version = VersionManager("1.2.3")
    version.minor()
    assert version.release() == "1.3.0"

def test_patch():
    version = VersionManager("1.2.3")
    version.patch()
    assert version.release() == "1.2.4"

def test_chain():
    version = VersionManager("1.2.3")
    version.major().minor().patch()
    assert version.release() == "2.1.1"

def test_rollback():
    version = VersionManager("1.2.3")
    version.major().minor().patch()
    assert version.release() == "2.1.1"
    version.rollback()
    assert version.release() == "2.1.0"
    version.rollback()
    assert version.release() == "2.0.0"
    version.rollback()
    assert version.release() == "1.2.3"

    with pytest.raises(Exception) as excinfo:
        version.rollback()
    assert str(excinfo.value) == "Cannot rollback!"
