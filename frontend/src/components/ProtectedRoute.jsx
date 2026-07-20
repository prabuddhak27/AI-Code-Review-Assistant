import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="px-6 py-16 text-mist/60">Loading…</div>;
  if (!user) return <Navigate to="/login" replace />;
  return children;
}
