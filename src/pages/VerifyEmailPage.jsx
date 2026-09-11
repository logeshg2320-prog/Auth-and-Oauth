import { useState, useRef } from "react";
import { useLocation, Link, useNavigate } from "react-router-dom";
import { ShieldCheck } from "lucide-react";
import AuthCard from "../components/AuthCard";
import Button from "../components/Button";
import { useToast } from "../components/Toast";
import API from "../api";

export default function VerifyEmailPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const toast = useToast();
  const email = location.state?.email || "";
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const [loading, setLoading] = useState(false);
  const inputRefs = useRef([]);

  function handleChange(index, value) {
    if (!/^\d*$/.test(value)) return;
    const newOtp = [...otp];
    newOtp[index] = value.slice(-1);
    setOtp(newOtp);
    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  }

  function handleKeyDown(index, e) {
    if (e.key === "Backspace" && !otp[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  }

  function handlePaste(e) {
    e.preventDefault();
    const pasted = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, 6);
    if (pasted.length === 6) {
      setOtp(pasted.split(""));
      inputRefs.current[5]?.focus();
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const code = otp.join("");
    if (code.length !== 6) {
      toast.error("Please enter the full 6-digit code");
      return;
    }
    setLoading(true);
    try {
      const res = await API.post("/verify-email", { email, otp: code });
      toast.success(res.data.message);
      navigate("/login");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Verification failed");
    } finally {
      setLoading(false);
    }
  }

  if (!email) {
    return (
      <AuthCard title="Verify Email" subtitle="No email address provided">
        <div className="auth-links">
          <Link to="/signup">Go to Signup</Link>
        </div>
      </AuthCard>
    );
  }

  return (
    <AuthCard
      title="Verify Email"
      subtitle={`Enter the 6-digit code sent to ${email}`}
      icon={<ShieldCheck />}
    >
      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="otp-inputs" onPaste={handlePaste}>
          {otp.map((digit, i) => (
            <input
              key={i}
              ref={(el) => (inputRefs.current[i] = el)}
              type="text"
              inputMode="numeric"
              maxLength={1}
              className="otp-input"
              value={digit}
              onChange={(e) => handleChange(i, e.target.value)}
              onKeyDown={(e) => handleKeyDown(i, e)}
              autoFocus={i === 0}
            />
          ))}
        </div>

        <Button type="submit" variant="primary" loading={loading} className="w-full">
          Verify Email
        </Button>
      </form>

      <div className="auth-links">
        Didn't receive the code? <Link to="/signup">Resend</Link>
      </div>
    </AuthCard>
  );
}
