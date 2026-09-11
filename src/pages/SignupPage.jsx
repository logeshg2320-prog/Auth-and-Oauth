import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Mail, Lock, UserPlus } from "lucide-react";
import AuthCard from "../components/AuthCard";
import InputField from "../components/InputField";
import Button from "../components/Button";
import { useToast } from "../components/Toast";
import API from "../api";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const toast = useToast();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await API.post("/signup", { email, password });
      toast.success(res.data.message);
      navigate("/verify-email", { state: { email } });
    } catch (err) {
      toast.error(err.response?.data?.detail || "Signup failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthCard
      title="Create Account"
      subtitle="Join us and get started"
      icon={<UserPlus />}
    >
      <form className="auth-form" onSubmit={handleSubmit}>
        <InputField
          label="Email Address"
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
          placeholder="Create a strong password"
          icon={Lock}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <Button type="submit" variant="gold" loading={loading} className="w-full">
          Create Account
        </Button>
      </form>

      <div className="auth-links">
        Already have an account? <Link to="/login">Sign in</Link>
      </div>
    </AuthCard>
  );
}
