import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./AuthContext";
import { PageLoader } from "../components/feedback/Spinner";

export function ProtectedRoute() {
  const { user, bootstrapping } = useAuth();
  if (bootstrapping) return <PageLoader message="Checking session…" />;
  if (!user) return <Navigate to="/login" replace />;
  return <Outlet />;
}
