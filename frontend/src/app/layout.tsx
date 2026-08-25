import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Governance Readiness Assessment",
  description:
    "Assess your organization's readiness to govern AI responsibly. Results support governance planning and are not legal advice or certification.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
