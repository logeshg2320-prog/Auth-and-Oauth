import { useState } from "react";
import { Link } from "react-router-dom";
import { Mail, Lock, LogIn } from "lucide-react";
import AuthCard from "../components/AuthCard";
import InputField from "../components/InputField";
import Button from "../components/Button";
import { useToast } from "../components/Toast";
import { useAuth } from "../context/AuthContext";
import API from "../api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const toast = useToast();
  const { login } = useAuth();

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    try {
      // Backend expects OAuth2PasswordRequestForm (form-urlencoded)
      const params = new URLSearchParams();
      params.append("username", email);
      params.append("password", password);

      const res = await API.post("/login", params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      toast.success("Welcome back! Logging you in...");
      login(res.data.access_token);
    } catch (err) {
      toast.error(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  function handleGoogleLogin() {
    window.location.href = "http://localhost:8000/login/google";
  }

  return (
    <AuthCard
      title="Welcome Back"
      subtitle="Sign in to your account"
      icon={<LogIn />}
    >
      <form className="auth-form" onSubmit={handleSubmit}>
        <InputField
          label="Email"
          type="email"
          placeholder="you@example.com"
          icon={Mail}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <InputField
          label="Password"
          type="password"
          placeholder="Enter your password"
          icon={Lock}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <div className="forgot-link">
          <Link to="/forgot-password">Forgot password?</Link>
        </div>

        <Button type="submit" variant="primary" loading={loading} className="w-full">
          Sign In
        </Button>

        <div className="divider">or</div>

        <Button variant="google" onClick={handleGoogleLogin} className="w-full">
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" />
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
          </svg>
          Continue with Google
        </Button>
      </form>

      <div className="auth-links">
        Don't have an account? <Link to="/signup">Create one</Link>
      </div>
    </AuthCard>
  );
}
