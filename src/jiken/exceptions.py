class ReinfoLibError(Exception):
    """Base exception for ReinfoLib errors."""


class ReinfoLibAuthError(ReinfoLibError):
    """Authentication error (401 Unauthorized)."""


class ReinfoLibRequestError(ReinfoLibError):
    """Invalid request parameters (400 Bad Request)."""


class ReinfoLibAPIError(ReinfoLibError):
    """General API error (5xx)."""
