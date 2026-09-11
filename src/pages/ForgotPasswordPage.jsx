import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Mail, KeyRound } from "lucide-react";
import AuthCard from "../components/AuthCard";
import InputField from "../components/InputField";
import Button from "../components/Button";
import { useToast } from "../components/Toast";
import API from "../api";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const toast = useToast();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await API.post("/forgot-password", { email });
      toast.success(res.data.message);
      navigate("/reset-password", { state: { email } });
    } catch (err) {
      toast.error(err.response?.data?.detail || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthCard
      title="Forgot Password"
      subtitle="Enter your email to receive a reset code"
      icon={<KeyRound />}
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

        <Button type="submit" variant="primary" loading={loading} className="w-full">
          Send Reset Code
        </Button>
      </form>

      <div className="auth-links">
        Remember your password? <Link to="/login">Sign in</Link>
      </div>
    </AuthCard>
  );
}
