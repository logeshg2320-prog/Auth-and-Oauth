# Auth-and-Oauth
Created a JWT auth and Google Oauth2
<<<<<<< HEAD
# Auth-and-Oauth
Created a JWT auth and Google Oauth2
=======
# AuthFlow Frontend

## Run
```bash
npm install
cp .env.example .env
npm run dev
```

Backend expected at `http://127.0.0.1:8000`.

## Backend endpoints used
- POST /signup
- POST /verify-email
- POST /login (OAuth2 form-urlencoded)
- GET /me
- POST /forgot-password
- POST /reset-password

Google OAuth URL is configurable with `VITE_GOOGLE_AUTH_URL`.
>>>>>>> 02fc5df (Initial commit without env file)

