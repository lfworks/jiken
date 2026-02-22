import pytest

from jiken.exceptions import (
    JikenAPIError,
    JikenAuthError,
    JikenError,
    JikenRequestError,
)


def test_jiken_error_is_exception() -> None:
    assert issubclass(JikenError, Exception)


def test_jiken_auth_error_inheritance() -> None:
    assert issubclass(JikenAuthError, JikenError)
    assert issubclass(JikenAuthError, JikenError)
    assert issubclass(JikenAuthError, Exception)


def test_jiken_request_error_inheritance() -> None:
    assert issubclass(JikenRequestError, JikenError)
    assert issubclass(JikenRequestError, Exception)


def test_jiken_api_error_inheritance() -> None:
    assert issubclass(JikenAPIError, JikenError)
    assert issubclass(JikenAPIError, Exception)


def test_raise_jiken_error() -> None:
    with pytest.raises(JikenError) as exc_info:
        raise JikenError("Test error")

    assert str(exc_info.value) == "Test error"


def test_raise_jiken_auth_error() -> None:
    with pytest.raises(JikenAuthError) as exc_info:
        raise JikenAuthError("Authentication failed")

    assert str(exc_info.value) == "Authentication failed"


def test_raise_jiken_request_error() -> None:
    with pytest.raises(JikenRequestError) as exc_info:
        raise JikenRequestError("Invalid request")

    assert str(exc_info.value) == "Invalid request"


def test_raise_jiken_api_error() -> None:
    with pytest.raises(JikenAPIError) as exc_info:
        raise JikenAPIError("API error")

    assert str(exc_info.value) == "API error"


def test_catch_specific_error_as_base_error() -> None:
    with pytest.raises(JikenError):
        raise JikenAuthError("Auth error")

    with pytest.raises(JikenError):
        raise JikenRequestError("Request error")

    with pytest.raises(JikenError):
        raise JikenAPIError("API error")
