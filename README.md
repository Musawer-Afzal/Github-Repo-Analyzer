# GitHub Repository Analyzer

## Overview
This project is a web-based GitHub repository analytics tool built using FastAPI. It allows users to enter any GitHub username and get detailed insights about their public repositories including stars, forks, languages, activity trends, and a computed repository health score.

The application is built on top of the GitHub public API and enhances raw API data with structured analytics and visualizations that are not available directly on GitHub.

---

# Features
- GitHub user profile analysis
- Repository-level analytics (stars, forks, issues, size)
- Language distribution visualization
- Repository health scoring system
- Detection of inactive repositories
- Error handling for API failures and invalid inputs
- Optimized paginated fetching (improved performance using incremental loading)

---

# Tech Stack
- FastAPI (Backend framework)
- Jinja2 (HTML templating)
- HTTPX (Async API requests)
- TailwindCSS (UI styling)
- Chart.js (Data visualization)
- Python dotenv (Environment configuration)

---

# Setup Instructions

## 1. Clone Repository
```bash
git clone https://github.com/your-username/github-repo-analyzer.git
cd github-repo-analyzer
```

## 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Environment Variables
Create a .env file:
```python
GITHUB_TOKEN=your_github_token_here
API_TIMEOUT=10
```
**To get a GitHub token:**

1. Go to GitHub Settings
2. Developer Settings
3. Personal Access Tokens
4. Fine-grained tokens
5. Generate new token (classic)
6. Copy and paste into .env

## 5. Run Application
```python
python run.py
```
Then open:
[Github_Analyzer_App](http://127.0.0.1:8000)

## Project Structure
```bash
app/
├── main.py
├── routes/
├── services/
├── utils/
├── templates/
├── static/
├── models/
tests/
run.py
```

---

## Key Design Decisions
### Why FastAPI

FastAPI was chosen due to its async support, high performance, and simplicity in handling external API calls. It is well-suited for I/O heavy operations like GitHub API requests.

A worse choice would have been Flask without async support, as it would slow down concurrent API calls and reduce performance under multiple requests.

---

## Performance Optimization
The system was optimized to:

* Fetch only 20 repositories initially
* Load additional repositories in background batches
* Reduce blocking API calls
* This significantly reduced response time from approximately 4 seconds to around 1.5 seconds.

---

## Error Handling Strategy
The application handles:

* GitHub API rate limits
* Network timeouts
* Invalid usernames
* Missing repository fields (None values)
* Empty API responses

---

## Edge Case Handling
One handled edge case:

* File: <mark>app/services/github_service.py</mark>
* Case: Some repositories return None for description
* Fix: Safe fallback value applied before rendering

Without this handling, Jinja templates would crash due to slicing NoneType values.

---

## Known Limitations
* No persistent caching layer
* No database storage
* Limited pagination control on frontend scrolling behavior

---

## Future Improvements

* Add Redis caching for API responses
* Add database for historical analytics
* Improve pagination with infinite scroll UI
* Add authentication system for saved searches