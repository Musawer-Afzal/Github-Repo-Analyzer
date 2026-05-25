from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..services.github_service import GitHubService
from ..services.analytics_service import AnalyticsService
from ..utils.validators import validate_github_username
from ..utils.error_handlers import handle_github_error

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/analyze/{username}", response_class=HTMLResponse)
async def analyze_user(request: Request, username: str):
    # Validate input
    is_valid, error_msg = validate_github_username(username)
    if not is_valid:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "error": error_msg},
            status_code=400
        )
    
    try:
        # Fetch GitHub data
        github_service = GitHubService(request.app.state.client)
        analytics_service = AnalyticsService()
        
        user_data = await github_service.get_user_profile(username)
        repos_data = await github_service.get_user_repositories(username)
        
        # Calculate analytics
        analytics = analytics_service.calculate_all_analytics(repos_data)
        health_score = analytics_service.calculate_health_score(repos_data, user_data)
        
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "user": user_data,
                "repos": repos_data,
                "analytics": analytics,
                "health_score": health_score
            }
        )
        
    except HTTPException as e:
        error_message = handle_github_error(e.status_code)
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": error_message},
            status_code=e.status_code
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": "An unexpected error occurred. Please try again later."},
            status_code=500
        )