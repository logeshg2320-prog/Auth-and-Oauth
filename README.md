# Auth-and-Oauth

A full-stack authentication and authorization application built with a React frontend and Python backend.

The project demonstrates modern authentication concepts including JWT authentication, OAuth 2.0 / Google Login, email verification, password reset, OTP-based verification, protected routes, and user session management.

## 🚀 Features

### Authentication

- User registration
- User login
- JWT-based authentication
- Secure password handling
- Protected API endpoints
- Logout functionality
- Authentication state management

### Google OAuth

- Google Login
- OAuth 2.0 authorization flow
- Google OAuth callback handling
- Secure authentication using OAuth tokens
- Automatic user creation/login

### Email Verification

- Email verification flow
- Verification tokens
- OTP-based verification
- Resend verification functionality

### Password Management

- Forgot password
- Password reset
- Reset-password token validation
- Secure password update

### Frontend

- React
- Vite
- React Router
- Protected routes
- Authentication context
- Login and signup pages
- Dashboard
- Google callback page
- Password reset pages
- Email verification pages
- Responsive UI

### Backend

- Python
- FastAPI
- SQL database integration
- SQLAlchemy
- JWT
- OAuth 2.0
- Google OAuth
- Redis
- Email/OTP functionality
- Environment-based configuration

---

# 🏗️ Project Structure

```text
Auth-and-Oauth/
│
├── backend/
│   ├── auth.py
│   ├── db.py
│   ├── google_auth.py
│   ├── main.py
│   ├── otp.py
│   └── ...
│
├── src/
│   ├── components/
│   │   ├── Button.jsx
│   │   ├── InputField.jsx
│   │   ├── Navbar.jsx
│   │   ├── OTPInput.jsx
│   │   ├── ProtectedRoute.jsx
│   │   └── Toast.jsx
│   │
│   ├── context/
│   │   └── AuthContext.jsx
│   │
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── ForgotPassword.jsx
│   │   ├── ForgotPasswordPage.jsx
│   │   ├── GoogleCallbackPage.jsx
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── LoginPage.jsx
│   │   ├── ResetPassword.jsx
│   │   ├── ResetPasswordPage.jsx
│   │   ├── Signup.jsx
│   │   ├── SignupPage.jsx
│   │   ├── VerifyEmail.jsx
│   │   └── VerifyEmailPage.jsx
│   │
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
│
├── .env
├── .gitignore
├── package.json
├── vite.config.js
└── README.md