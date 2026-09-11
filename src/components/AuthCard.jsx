import { Shield } from "lucide-react";

export default function AuthCard({ title, subtitle, icon, children }) {
  return (
    <div className="auth-card">
      <div className="brand">
        <div className="brand-icon">
          {icon || <Shield />}
        </div>
        <h1>{title}</h1>
        {subtitle && <p>{subtitle}</p>}
      </div>
      {children}
    </div>
  );
}
