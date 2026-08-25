import Link from "next/link";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
  href?: string;
}

const styles = {
  primary:
    "bg-[var(--color-primary)] text-white hover:bg-[var(--color-primary-light)] focus-visible:ring-2 focus-visible:ring-[var(--color-primary)] focus-visible:ring-offset-2",
  secondary:
    "border border-[var(--color-primary)] text-[var(--color-primary)] hover:bg-slate-50 focus-visible:ring-2 focus-visible:ring-[var(--color-primary)] focus-visible:ring-offset-2",
  ghost:
    "text-[var(--color-primary)] hover:bg-slate-100 focus-visible:ring-2 focus-visible:ring-[var(--color-primary)] focus-visible:ring-offset-2",
};

export function Button({ variant = "primary", href, className = "", children, ...props }: ButtonProps) {
  const classes = `inline-flex items-center justify-center rounded-md px-5 py-2.5 text-sm font-medium transition-colors disabled:opacity-50 ${styles[variant]} ${className}`;

  if (href) {
    return (
      <Link href={href} className={classes}>
        {children}
      </Link>
    );
  }

  return (
    <button className={classes} {...props}>
      {children}
    </button>
  );
}
