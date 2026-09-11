import { useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../components/Toast";

export default function GoogleCallbackPage() {
  const [searchParams] = useSearchParams();
  const { login } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    const token = searchParams.get("access_token");

    if (token) {
      toast.success("Google login successful!");
      login(token);
    } else {
      toast.error("Google login failed — no token received");
      navigate("/login");
    }
  }, []);

  return (
    <div className="loading-overlay">
      <div className="loading-spinner" />
    </div>
  );
}
