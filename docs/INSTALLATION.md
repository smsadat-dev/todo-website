# Installation & Setup guide
### This document explain how to build the website from source. Follow each steps carefully to build.

## 1. Prerequisites
Make sure to have the following installed
1. Python3.10+
2. PostgreSQL 14+ 
3. Git 
4. Docker and Docker compose
## 2. Clone the repository 
````
git clone https://github.com/smsadat-dev/todo-website.git
cd todo-website
````

## 3. Backend Setup (Django + PostgreSQL)
### Create virtual environment 
````
python3 -m venv .venv
source .venv/bin/activate # for linux (don't care bout windows 🚬)
````
 ### Install dependencies 
 `` pip install -r requirements.txt ``
 ### Configure environment variable 
 ````
	DEBUG=True
	SECRET_KEY=<your secret key>
	# Database (Postgres)
	DATABASE_URL=postgres://<db_user>:<db_password>@localhost:5432/<db_name>

	CORS / Allowed Hosts
	ALLOWED_HOSTS=127.0.0.1,localhost
	CORS_ALLOWED_ORIGINS=http://127.0.0.1:5500,http://localhost:5500

	Google OAuth
	GOOGLE_CLIENT_ID=your-google-client-id
	GOOGLE_CLIENT_SECRET=your-google-client-secret
````

### Setup database
`` python3 manage.py migrate ``
The backend will run at: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

## 4. Frontend Setup (Static SPA)

The frontend is plain HTML, CSS, and JS. No build tools required.

### Run local static server
````
cd frontend
python3 -m http.server 5500
````

Now open http://127.0.0.1:5500/index.html
in your browser.
The frontend will connect to the backend via CORS.

## 5. Google OAuth Setup

1.  Go to Google Cloud Console-   Create an **OAuth 2.0 Client ID**.
    
2.  Add these redirect URIs:
`` http://127.0.0.1:8000/api/auth/google/callback/``
3. Copy the Client ID and Secret into your .env.

 
 
 


