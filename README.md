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
