from fastapi import HTTPException
import httpx
import os
from datetime import datetime, timezone

class GitHubService:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.base_url = "https://api.github.com"
        self.headers = {}
        
        # Add token if available
        token = os.getenv("GITHUB_TOKEN")
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
    
    async def get_user_profile(self, username: str) -> dict:
        try:
            response = await self.client.get(
                f"{self.base_url}/users/{username}",
                headers=self.headers
            )
            
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="User not found")
            elif response.status_code == 403:
                raise HTTPException(status_code=403, detail="Rate limit exceeded. Please try again later.")
            elif response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="GitHub API error")
            
            data = response.json()
            
            # Calculate account age
            created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            account_age_days = (
                datetime.now(timezone.utc) -
                created_at.replace(tzinfo=timezone.utc)
            ).days
            
            return {
                "login": data['login'],
                "name": data.get('name', 'Not provided'),
                "avatar_url": data['avatar_url'],
                "bio": data.get('bio', 'No bio provided'),
                "followers": data['followers'],
                "following": data['following'],
                "public_repos": data['public_repos'],
                "created_at": data['created_at'],
                "account_age_days": account_age_days,
                "html_url": data['html_url']
            }
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="GitHub API timeout. Please try again.")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Cannot reach GitHub API. Please try again later.")
    
    async def get_user_repositories(
        self,
        username: str,
        page: int = 1,
        per_page: int = 20
    ) -> list:
        try:
            response = await self.client.get(
                f"{self.base_url}/users/{username}/repos",
                headers=self.headers,
                params={
                    "per_page": per_page,
                    "page": page,
                    "sort": "updated"
                }
            )
            
            if response.status_code != 200:
                return []
            
            repos = response.json()
            
            # Fetch additional data for each repo (languages, contributors)
            enriched_repos = []
            for repo in repos[:30]:  # Limit to 30 repos for performance
                enriched = {
                    "name": repo['name'],
                    "description": repo.get('description') or 'No description available',
                    "stars": repo['stargazers_count'],
                    "forks": repo['forks_count'],
                    "open_issues": repo['open_issues_count'],
                    "size_kb": repo['size'],
                    "language": repo.get('language') or 'Unknown',
                    "updated_at": repo['updated_at'],
                    "html_url": repo['html_url'],
                    "created_at": repo['created_at']
                }
                
                # Get languages for this repo
                # enriched["languages"] = await self._get_repo_languages(username, repo['name'])
                enriched_repos.append(enriched)
            
            return enriched_repos
            
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="GitHub API timeout. Please try again.")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Cannot reach GitHub API. Please try again later.")
    
    async def _get_repo_languages(self, owner: str, repo: str) -> dict:
        try:
            response = await self.client.get(
                f"{self.base_url}/repos/{owner}/{repo}/languages",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}