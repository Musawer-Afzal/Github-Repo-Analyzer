def handle_github_error(status_code: int) -> str:
    """Convert GitHub API error codes to user-friendly messages"""
    error_messages = {
        400: "Bad request. Please check the username and try again.",
        401: "Authentication failed. Please try again later.",
        403: "Rate limit exceeded. Please wait a few minutes before trying again.",
        404: "GitHub user not found. Please check the username and try again.",
        408: "Request timeout. Please try again.",
        500: "GitHub API is experiencing issues. Please try again later.",
        502: "GitHub API is temporarily unavailable. Please try again later.",
        503: "GitHub API is unavailable. Please try again later.",
        504: "GitHub API timed out. Please try again."
    }
    
    return error_messages.get(status_code, f"An error occurred (HTTP {status_code}). Please try again.")