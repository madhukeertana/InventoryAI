import { type InputHTMLAttributes, forwardRef } from "react";
import { cn } from "../../lib/cn";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, className, id, ...props }, ref) => {
    const inputId = id ?? label.toLowerCase().replace(/\s+/g, "-");
    return (
      <label className="flex w-full flex-col gap-1.5 text-sm" htmlFor={inputId}>
        <span className="font-medium text-primary">{label}</span>
        <input
          ref={ref}
          id={inputId}
          className={cn(
            "rounded-lg border border-primary-30 bg-surface-elevated px-3 py-2.5 text-primary outline-none transition placeholder:text-primary-60 focus:border-primary focus:ring-2 focus:ring-primary/15",
            className,
          )}
          {...props}
        />
      </label>
    );
  },
);

Input.displayName = "Input";
