import { type FormEvent, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuth } from "../auth/AuthContext";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { PageLoader } from "../components/feedback/Spinner";
import { navIcons } from "../icons";
import { ApiError } from "../api/client";

export function LoginPage() {
  const { user, bootstrapping, login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("owner@retail.example");
  const [password, setPassword] = useState("Password123!");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (bootstrapping) return <PageLoader message="Loading…" />;
  if (user) return <Navigate to="/actions" replace />;

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
      navigate("/actions");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-surface px-4">
      <div
        className="pointer-events-none absolute inset-0 opacity-40"
        style={{
          backgroundImage:
            "radial-gradient(circle at 20% 20%, rgba(11,58,74,0.12), transparent 45%), radial-gradient(circle at 80% 80%, rgba(11,58,74,0.1), transparent 40%)",
        }}
      />
      <motion.div
        className="relative w-full max-w-md rounded-2xl bg-surface-elevated p-8 shadow-sm ring-1 ring-primary-30"
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <p className="font-display text-3xl font-semibold tracking-tight text-primary">
          PharmaStock AI
        </p>
        <p className="mt-2 text-sm text-primary-80">
          Know what you have. Predict what you need. Act today.
        </p>
        <form className="mt-8 space-y-4" onSubmit={onSubmit}>
          <Input
            label="Email"
            type="email"
            autoComplete="username"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <Input
            label="Password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && (
            <p className="text-sm font-medium text-primary" role="alert">
              {error}
            </p>
          )}
          <Button className="w-full" type="submit" loading={loading} icon={navIcons.login}>
            Sign in
          </Button>
        </form>
        <p className="mt-6 text-xs text-primary-60">
          Demo: owner@retail.example / Password123!
        </p>
      </motion.div>
    </div>
  );
}
