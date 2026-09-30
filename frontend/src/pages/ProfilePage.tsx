import { User as UserIcon } from "lucide-react";
import { useAuth } from "../auth/AuthContext";
import { PageHeader } from "../components/ui/PageHeader";
import { roleLabels } from "../icons";

export function ProfilePage() {
  const { user } = useAuth();
  if (!user) return null;

  return (
    <div>
      <PageHeader
        icon={UserIcon}
        title="Profile"
        subtitle="Session identity from your HttpOnly cookie — no token stored in the browser."
      />
      <dl className="grid gap-4 rounded-2xl bg-surface-elevated p-5 ring-1 ring-primary-30 sm:grid-cols-2">
        <div>
          <dt className="text-xs font-semibold uppercase tracking-wide text-primary-60">Name</dt>
          <dd className="mt-1 font-medium">{user.full_name}</dd>
        </div>
        <div>
          <dt className="text-xs font-semibold uppercase tracking-wide text-primary-60">Email</dt>
          <dd className="mt-1 font-medium">{user.email}</dd>
        </div>
        <div>
          <dt className="text-xs font-semibold uppercase tracking-wide text-primary-60">Role</dt>
          <dd className="mt-1 font-medium">{roleLabels[user.role]}</dd>
        </div>
        <div>
          <dt className="text-xs font-semibold uppercase tracking-wide text-primary-60">Organization</dt>
          <dd className="mt-1 font-medium break-all text-sm">{user.organization_id ?? "—"}</dd>
        </div>
      </dl>
    </div>
  );
}
