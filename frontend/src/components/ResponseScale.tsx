"use client";

import { RESPONSE_OPTIONS } from "@/types/assessment";

interface ResponseScaleProps {
  name: string;
  value: number | undefined;
  onChange: (value: number) => void;
}

export function ResponseScale({ name, value, onChange }: ResponseScaleProps) {
  return (
    <fieldset>
      <legend className="sr-only">Response</legend>
      <div className="grid gap-2 sm:grid-cols-2">
        {RESPONSE_OPTIONS.map((option) => {
          const id = `${name}-${option.value}`;
          return (
            <label
              key={option.value}
              htmlFor={id}
              className={`flex cursor-pointer items-center gap-2 rounded-md border px-3 py-2 text-sm transition-colors ${
                value === option.value
                  ? "border-[var(--color-primary)] bg-slate-50 ring-1 ring-[var(--color-primary)]"
                  : "border-slate-200 hover:border-slate-300"
              }`}
            >
              <input
                id={id}
                type="radio"
                name={name}
                value={option.value}
                checked={value === option.value}
                onChange={() => onChange(option.value)}
                className="text-[var(--color-primary)] focus:ring-[var(--color-primary)]"
              />
              <span>{option.label}</span>
            </label>
          );
        })}
      </div>
    </fieldset>
  );
}
