# oauth.py
"""
OAuth token exchange simulation for TikTok Ads API

This module mimics real-world OAuth behavior:
- Authorization code exchange
- Scope validation
- Clear error explanations
- Actionable retry guidance

────────────────────────────────────────────
ACCURACY EXAMPLES (EXPECTED BEHAVIOR)
────────────────────────────────────────────

Example 1: Invalid client credentials
Input:
    exchange_code_for_token("bad_client")

Raises:
    OAuthException(
        error="Invalid client credentials",
        explanation="Client ID or secret is incorrect.",
        action="Verify TikTok Ads app credentials.",
        retry=False
    )

────────────────────────────────────────────

Example 2: Missing required scopes
Input:
    exchange_code_for_token("no_scope")

Raises:
    OAuthException(
        error="Missing permission",
        explanation="Ads permission scope not granted.",
        action="Reauthorize with ads.read and ads.write scopes.",
        retry=False
    )

────────────────────────────────────────────

Example 3: Successful token exchange
Input:
    exchange_code_for_token("valid_code")

Returns:
{
    "access_token": "mock_access_token",
    "token_type": "Bearer",
    "expires_in": 3600,
    "scopes": ["ads.read", "ads.write"]
}

────────────────────────────────────────────
"""


class OAuthException(Exception):
    """
    Structured OAuth error for API-safe handling
    """

    def __init__(self, error, explanation, action, retry):
        self.error = error
        self.explanation = explanation
        self.action = action
        self.retry = retry

    def to_dict(self):
        """
        Convert exception into API-friendly response
        """
        return {
            "error": self.error,
            "explanation": self.explanation,
            "action": self.action,
            "retry_allowed": self.retry
        }


def exchange_code_for_token(code: str):
    """
    Simulates authorization code → access token exchange
    """

    # ❌ Invalid client credentials
    if code == "bad_client":
        raise OAuthException(
            error="Invalid client credentials",
            explanation="Client ID or secret is incorrect.",
            action="Verify TikTok Ads app credentials.",
            retry=False
        )

    # ❌ Missing permission scopes
    if code == "no_scope":
        raise OAuthException(
            error="Missing permission",
            explanation="Ads permission scope not granted.",
            action="Reauthorize with ads.read and ads.write scopes.",
            retry=False
        )

    # ❌ Expired authorization code
    if code == "expired_code":
        raise OAuthException(
            error="Authorization code expired",
            explanation="The authorization code is no longer valid.",
            action="Restart OAuth login flow.",
            retry=True
        )

    # ✅ Successful token exchange
    return {
        "access_token": "mock_access_token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "scopes": ["ads.read", "ads.write"]
    }
