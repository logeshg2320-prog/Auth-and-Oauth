import { useAuth } from "../context/AuthContext";
import { Mail, Shield, Clock, LogOut } from "lucide-react";
import Button from "../components/Button";

export default function DashboardPage() {
  const { user, logout } = useAuth();

  return (
    <div className="dashboard">
      <div className="dashboard-card">
        <div className="dashboard-header">
          <div className="dashboard-greeting">
            <h1>Welcome</h1>
            <p>Your secure account dashboard</p>
          </div>
          <Button variant="danger" onClick={logout}>
            <LogOut size={16} />
            Logout
          </Button>
        </div>

        <div className="dashboard-content">
          <div className="dashboard-stat">
            <div className="stat-icon purple">
              <Mail size={20} />
            </div>
            <div>
              <div className="stat-label">Email Address</div>
              <div className="stat-value">{user?.email || "Loading..."}</div>
            </div>
          </div>

          <div className="dashboard-stat">
            <div className="stat-icon gold">
              <Shield size={20} />
            </div>
            <div>
              <div className="stat-label">Account Status</div>
              <div className="stat-value">Verified ✓</div>
            </div>
          </div>

          <div className="dashboard-stat">
            <div className="stat-icon emerald">
              <Clock size={20} />
            </div>
            <div>
              <div className="stat-label">Session</div>
              <div className="stat-value">Active — JWT Authenticated</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
