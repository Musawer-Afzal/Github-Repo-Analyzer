def format_number(num: int) -> str:
    """Format large numbers with K, M suffixes"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

def format_date(date_string: str) -> str:
    """Format ISO date to readable format"""
    from datetime import datetime
    try:
        date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return date.strftime("%B %d, %Y")
    except:
        return date_string