import "./globals.css";
export const metadata = { title: "Synexa Growth OS", description: "AI Executive Leadership Team" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
