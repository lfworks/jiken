import pytest

from pyreinfolib.exceptions import (
    ReinfoLibAPIError,
    ReinfoLibAuthError,
    ReinfoLibError,
    ReinfoLibRequestError,
)


def test_reinfolib_error_is_exception() -> None:
    assert issubclass(ReinfoLibError, Exception)


def test_reinfolib_auth_error_inheritance() -> None:
    assert issubclass(ReinfoLibAuthError, ReinfoLibError)
    assert issubclass(ReinfoLibAuthError, ReinfoLibError)
    assert issubclass(ReinfoLibAuthError, Exception)


def test_reinfolib_request_error_inheritance() -> None:
    assert issubclass(ReinfoLibRequestError, ReinfoLibError)
    assert issubclass(ReinfoLibRequestError, Exception)


def test_reinfolib_api_error_inheritance() -> None:
    assert issubclass(ReinfoLibAPIError, ReinfoLibError)
    assert issubclass(ReinfoLibAPIError, Exception)


def test_raise_reinfolib_error() -> None:
    with pytest.raises(ReinfoLibError) as exc_info:
        raise ReinfoLibError("Test error")

    assert str(exc_info.value) == "Test error"


def test_raise_reinfolib_auth_error() -> None:
    with pytest.raises(ReinfoLibAuthError) as exc_info:
        raise ReinfoLibAuthError("Authentication failed")

    assert str(exc_info.value) == "Authentication failed"


def test_raise_reinfolib_request_error() -> None:
    with pytest.raises(ReinfoLibRequestError) as exc_info:
        raise ReinfoLibRequestError("Invalid request")

    assert str(exc_info.value) == "Invalid request"


def test_raise_reinfolib_api_error() -> None:
    with pytest.raises(ReinfoLibAPIError) as exc_info:
        raise ReinfoLibAPIError("API error")

    assert str(exc_info.value) == "API error"


def test_catch_specific_error_as_base_error() -> None:
    with pytest.raises(ReinfoLibError):
        raise ReinfoLibAuthError("Auth error")

    with pytest.raises(ReinfoLibError):
        raise ReinfoLibRequestError("Request error")

    with pytest.raises(ReinfoLibError):
        raise ReinfoLibAPIError("API error")
