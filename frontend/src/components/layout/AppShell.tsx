import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuth } from "../../auth/AuthContext";
import { Button } from "../ui/Button";
import { navIcons, roleLabels } from "../../icons";
import { cn } from "../../lib/cn";

const links = [
  { to: "/actions", label: "Today's Actions", icon: navIcons.actions },
  { to: "/inventory", label: "Inventory", icon: navIcons.inventory },
  { to: "/ocr", label: "Inward OCR", icon: navIcons.ocr },
  { to: "/profile", label: "Profile", icon: navIcons.profile },
];

export function AppShell() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-surface text-primary">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col md:flex-row">
        <aside className="hidden w-64 shrink-0 border-r border-primary-30 bg-surface-elevated md:flex md:flex-col">
          <div className="border-b border-primary-30 px-5 py-6">
            <p className="font-display text-xl font-semibold tracking-tight">PharmaStock AI</p>
            <p className="mt-1 text-xs text-primary-80">Action-first inventory</p>
          </div>
          <nav className="flex flex-1 flex-col gap-1 p-3">
            {links.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition",
                    isActive
                      ? "bg-primary text-surface"
                      : "text-primary-80 hover:bg-surface hover:text-primary",
                  )
                }
              >
                <Icon className="h-4 w-4" aria-hidden />
                {label}
              </NavLink>
            ))}
          </nav>
          <div className="border-t border-primary-30 p-4">
            <p className="truncate text-sm font-semibold">{user?.full_name}</p>
            <p className="truncate text-xs text-primary-80">
              {user ? roleLabels[user.role] : ""}
            </p>
            <Button
              className="mt-3 w-full"
              variant="outline"
              icon={navIcons.logout}
              onClick={async () => {
                await logout();
                navigate("/login");
              }}
            >
              Log out
            </Button>
          </div>
        </aside>

        <div className="flex min-w-0 flex-1 flex-col">
          <header className="flex items-center justify-between border-b border-primary-30 bg-surface-elevated px-4 py-3 md:hidden">
            <p className="font-display text-lg font-semibold">PharmaStock AI</p>
            <Button
              variant="ghost"
              icon={navIcons.logout}
              aria-label="Log out"
              onClick={async () => {
                await logout();
                navigate("/login");
              }}
            >
              Out
            </Button>
          </header>

          <motion.main
            className="relative flex-1 px-4 py-6 md:px-8"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25 }}
          >
            <Outlet />
          </motion.main>

          <nav className="sticky bottom-0 grid grid-cols-4 border-t border-primary-30 bg-surface-elevated md:hidden">
            {links.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  cn(
                    "flex flex-col items-center gap-1 px-1 py-2 text-[10px] font-medium",
                    isActive ? "text-primary" : "text-primary-60",
                  )
                }
              >
                <Icon className="h-5 w-5" aria-hidden />
                <span className="truncate">{label.split(" ")[0]}</span>
              </NavLink>
            ))}
          </nav>
        </div>
      </div>
    </div>
  );
}
