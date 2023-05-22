### Hexlet tests and linter status:  
[![Actions Status](https://github.com/NikolayZemelko/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/NikolayZemelko/python-project-83/actions)  
[![Actions Status](https://github.com/NikolayZemelko/python-project-83/workflows/main-check/badge.svg)](https://github.com/NikolayZemelko/python-project-83/actions)  
[![Maintainability](https://api.codeclimate.com/v1/badges/594e0c67d9bc329208a4/maintainability)](https://codeclimate.com/github/NikolayZemelko/python-project-83/maintainability)  
  **Pages Analyser** is a web application for checking the availability of URLs. The application keeps a history of checks.
  
[https://python-project-83-production-7eef.up.railway.app](https://python-project-83-production-7eef.up.railway.app)

## Table of Contents

 - [Stack](https://github.com/NikolayZemelko/python-project-83#stack)
 - [Setup](https://github.com/NikolayZemelko/python-project-83#setup)
 - 
## Stack
 - Flask (Developer server)
 - Gunicorn (Production server)
 - Bootstrap 5 (Frontend toolkit)
 - Requests (HTTP library)
 - Python-dotenv (Environment variable management)
 - Flake8 (Code linter)
 - PostgreSQL (Database)
 - Psycorg (To work with database)
 - Railway (Deployment service)
 - BeautifulSoup (SEO analysis)

## Setup

Requirments installed and configured:
- PostgreSQL
- Python
- Poetry

1. Clone this repository.
2. Add `.env` file into project root.
3. Add Environment Variables DATABASE_URL and SECRET_KEY into the `.env` file.
4. Install dependecies: `make install`.
5. Run for developer: `make dev`.
6. Run for production: `make start`.