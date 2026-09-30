import type { LucideIcon } from "lucide-react";

interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description: string;
}

export function EmptyState({ icon: Icon, title, description }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-primary-30 bg-surface-elevated px-6 py-14 text-center">
      <Icon className="mb-3 h-8 w-8 text-primary-60" aria-hidden />
      <h3 className="text-base font-semibold text-primary">{title}</h3>
      <p className="mt-1 max-w-sm text-sm text-primary-80">{description}</p>
    </div>
  );
}
