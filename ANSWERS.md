## 1. How to run
### Steps
```bash
pip install -r requirements.txt
python run.py
```

Open:
[Github_Analyzer_App](http://127.0.0.1:8000)

If GitHub API token is required:

**To get a GitHub token:**

1. Go to GitHub Settings
2. Developer Settings
3. Personal Access Tokens
4. Fine-grained tokens
5. Generate new token (classic)
6. Copy and paste into .env

Create .env
Add:
```python
GITHUB_TOKEN=your_token_here
```

## 2. Stack Choice
**Chosen Stack**
* FastAPI
* Jinja2
* HTTPX
* Chart.js

**Reason**
FastAPI allows async API calls which is critical when calling GitHub API multiple times per request. This reduces latency and improves responsiveness.

Jinja2 allows server-side rendering which keeps the project simple and fast without needing a frontend framework.

Worse Choice

Flask would be worse because it is synchronous by default and would slow down multiple GitHub API calls. A full React frontend would also be unnecessary overhead for this assessment.

3. One real edge case
Edge Case

Some GitHub repositories return null for optional fields like description.

Location
app/services/github_service.py
Handling

Default fallback values are assigned:

description → "No description"
Without Fix

The Jinja template would crash when trying to slice NoneType values.

4. AI Usage
AI Tools Used
ChatGPT for architecture design
ChatGPT for bug fixing (datetime offset issue)
ChatGPT for performance optimization strategy
Example Modification

AI suggested fetching 30 repositories at once. This was modified to:

Fetch 20 initially
Load remaining asynchronously

Reason: Improved perceived performance and reduced initial latency.

5. Honest Gap
Weak Area

The project does not currently use caching or persistent storage.

Impact

Repeated requests to GitHub API may be slow and subject to rate limits.

Fix

Add Redis caching layer or local database (SQLite/PostgreSQL) to store:

User profiles
Repository metadata
Analytics results

This would reduce API dependency and improve scalability.