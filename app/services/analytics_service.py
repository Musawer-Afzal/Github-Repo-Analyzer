from datetime import datetime
from collections import Counter

class AnalyticsService:
    def calculate_all_analytics(self, repos: list) -> dict:
        if not repos:
            return {
                "total_stars": 0,
                "total_forks": 0,
                "top_starred_repo": None,
                "most_forked_repo": None,
                "language_distribution": {},
                "inactive_repos": [],
                "average_repo_size": 0,
                "repos_with_issues": 0
            }
        
        total_stars = sum(repo['stars'] for repo in repos)
        total_forks = sum(repo['forks'] for repo in repos)
        
        # Find top repos
        top_starred = max(repos, key=lambda x: x['stars']) if repos else None
        most_forked = max(repos, key=lambda x: x['forks']) if repos else None
        
        # Language distribution
        languages = [repo['language'] for repo in repos if repo['language'] != 'Unknown']
        language_dist = dict(Counter(languages))
        
        # Inactive repos (no updates in 6 months)
        six_months_ago = datetime.now().timestamp() - (180 * 24 * 3600)
        inactive_repos = [
            repo['name'] for repo in repos
            if datetime.fromisoformat(repo['updated_at'].replace('Z', '+00:00')).timestamp() < six_months_ago
        ]
        
        # Average repo size
        avg_size = sum(repo['size_kb'] for repo in repos) / len(repos)
        
        # Repos with open issues
        repos_with_issues = sum(1 for repo in repos if repo['open_issues'] > 0)
        
        return {
            "total_stars": total_stars,
            "total_forks": total_forks,
            "top_starred_repo": top_starred,
            "most_forked_repo": most_forked,
            "language_distribution": language_dist,
            "inactive_repos": inactive_repos,
            "average_repo_size": round(avg_size, 2),
            "repos_with_issues": repos_with_issues
        }
    
    def calculate_health_score(self, repos: list, user_data: dict) -> dict:
        if not repos:
            return {"score": 0, "rating": "No Repositories", "details": {}}
        
        # Calculate health score components
        stars_score = min(sum(repo['stars'] for repo in repos) / 10, 30)
        forks_score = min(sum(repo['forks'] for repo in repos) / 5, 20)
        
        # Activity score (recent updates)
        recent_repos = sum(1 for repo in repos 
                          if (datetime.now() - datetime.fromisoformat(repo['updated_at'].replace('Z', '+00:00'))).days < 90)
        activity_score = (recent_repos / len(repos)) * 25
        
        # Issue management score
        repos_with_issues = sum(1 for repo in repos if repo['open_issues'] > 0)
        issue_score = ((len(repos) - repos_with_issues) / len(repos)) * 15
        
        # Language diversity score
        languages = set(repo['language'] for repo in repos if repo['language'] != 'Unknown')
        diversity_score = min(len(languages) * 2, 10)
        
        total_score = stars_score + forks_score + activity_score + issue_score + diversity_score
        
        # Determine rating
        if total_score >= 80:
            rating = "Excellent"
        elif total_score >= 60:
            rating = "Good"
        elif total_score >= 40:
            rating = "Fair"
        elif total_score >= 20:
            rating = "Needs Improvement"
        else:
            rating = "Poor"
        
        return {
            "score": round(total_score, 2),
            "rating": rating,
            "details": {
                "stars_score": round(stars_score, 2),
                "forks_score": round(forks_score, 2),
                "activity_score": round(activity_score, 2),
                "issue_score": round(issue_score, 2),
                "diversity_score": diversity_score
            }
        }