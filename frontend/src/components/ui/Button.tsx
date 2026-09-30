import { type ButtonHTMLAttributes, type ReactNode } from "react";
import { Loader2, type LucideIcon } from "lucide-react";
import { cn } from "../../lib/cn";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "ghost" | "outline";
  loading?: boolean;
  icon?: LucideIcon;
  children: ReactNode;
}

export function Button({
  variant = "primary",
  loading,
  icon: Icon,
  className,
  disabled,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm font-semibold transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary disabled:cursor-not-allowed disabled:opacity-50",
        variant === "primary" && "bg-primary text-surface hover:bg-primary-80",
        variant === "outline" &&
          "border border-primary-30 bg-surface-elevated text-primary hover:bg-surface",
        variant === "ghost" && "text-primary hover:bg-primary/5",
        className,
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <Loader2 className="h-4 w-4 animate-spin" aria-hidden />
      ) : (
        Icon && <Icon className="h-4 w-4" aria-hidden />
      )}
      {children}
    </button>
  );
}
