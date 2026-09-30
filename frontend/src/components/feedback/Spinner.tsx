import { Loader2 } from "lucide-react";
import { cn } from "../../lib/cn";

interface SpinnerProps {
  className?: string;
  label?: string;
}

export function Spinner({ className, label = "Loading" }: SpinnerProps) {
  return (
    <span className="inline-flex items-center gap-2 text-primary" role="status" aria-live="polite">
      <Loader2 className={cn("h-5 w-5 animate-spin", className)} aria-hidden />
      <span className="sr-only">{label}</span>
    </span>
  );
}

export function PageLoader({ message = "Loading…" }: { message?: string }) {
  return (
    <div className="flex min-h-[50vh] flex-col items-center justify-center gap-3 text-primary">
      <Loader2 className="h-8 w-8 animate-spin" aria-hidden />
      <p className="text-sm text-primary-80">{message}</p>
    </div>
  );
}

export function LoadingOverlay({ message = "Loading data…" }: { message?: string }) {
  return (
    <div className="absolute inset-0 z-10 flex items-center justify-center bg-surface/80 backdrop-blur-[1px]">
      <div className="flex items-center gap-3 rounded-xl bg-surface-elevated px-4 py-3 shadow-sm ring-1 ring-primary-30">
        <Loader2 className="h-5 w-5 animate-spin text-primary" aria-hidden />
        <span className="text-sm font-medium text-primary">{message}</span>
      </div>
    </div>
  );
}
