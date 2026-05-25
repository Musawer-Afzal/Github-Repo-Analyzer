import re

def validate_github_username(username: str) -> tuple[bool, str]:
    """Validate GitHub username format"""
    if not username or not username.strip():
        return False, "Username cannot be empty"
    
    username = username.strip()
    
    if len(username) > 39:
        return False, "Username is too long (maximum 39 characters)"
    
    if len(username) < 1:
        return False, "Username is too short"
    
    # GitHub username regex: alphanumeric and hyphens, cannot start/end with hyphen
    pattern = r'^[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?$'
    
    if not re.match(pattern, username):
        return False, "Username can only contain letters, numbers, and hyphens (cannot start or end with hyphen)"
    
    return True, ""