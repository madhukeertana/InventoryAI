import type { LucideIcon } from "lucide-react";

interface PageHeaderProps {
  icon: LucideIcon;
  title: string;
  subtitle: string;
}

export function PageHeader({ icon: Icon, title, subtitle }: PageHeaderProps) {
  return (
    <header className="mb-6 flex items-start gap-3">
      <span className="mt-0.5 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary text-surface">
        <Icon className="h-5 w-5" aria-hidden />
      </span>
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-primary md:text-3xl">
          {title}
        </h1>
        <p className="mt-1 text-sm text-primary-80">{subtitle}</p>
      </div>
    </header>
  );
}
