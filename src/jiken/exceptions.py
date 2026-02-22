class JikenError(Exception):
    """Base exception for jiken errors."""


class JikenAuthError(JikenError):
    """Authentication error (401 Unauthorized)."""


class JikenRequestError(JikenError):
    """Invalid request parameters (400 Bad Request)."""


class JikenAPIError(JikenError):
    """General API error (5xx)."""
