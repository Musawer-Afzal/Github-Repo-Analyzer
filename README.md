# README.md

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