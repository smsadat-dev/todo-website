# Project architecture
## 1. Overview
This is a full-stack web application project with Django (REST-like) Backend and a vanilla Javascript frontend with SPA style frontend. 
Authentication is handled by JWT and Google Oauth2, backend and frontend communicate via CORS. 
## 2. High level diagram 
````
Frontend (HTML CSS JS) <---> AJAX/CORS <---> Backend (Django) <---> PostgreSQL
					|
					| -> Oauth redirect (Google Oauth2)
````
## 3. Repository structure
````
.github/workflows/
backend/
docs/
docker/
frontend/
tests/
README.md
LICENSE
````

## 4. Backend (Django)
- Framework: Django with JWT protection
- Database: PostgreSQL
- Keyapps:	
		- ``users/``-> Authentications w/JWT and Google Oauth
		- ``tasks/``-> Task CRUD APIs
- Endpoints:
	- `api/login/`
	- ``api/registration``
	- ``api/logout``
	- ``api/tasks/``
	- ``api/auth/google``
	- ``api/auth/google/login``
	- ``api/auth/google/callback``
## 5. Frontend (SPA)
- Built with vanilla Javascript (AJAX)
- All pages dynamically rendered 
- Communicate via fetch api
- All tokens stored in localstorage
## 6. Authentication flow 
1. User chooses default login or Google Oauth
2. On success:	
	- Backend issues JWT & refresh tokens
	- Tokens sorted in localstorage
3. All api calls include `` Authorization : Bearer <access token>`` 
4. Tokens can be refreshed or invalidate on logout 


## 7. Deployment
### Local development
- Backend: Run with ``python3 manage.py runserver ``
- Frontend: Open ``frontend/index.html`` in browser or via live server 






