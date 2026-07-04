import os
import json

root_dir = "/home/ruban/Documents/robovantha/hackathon/synexa-growth-os/frontend"

directories = [
    "src/app/(auth)/login",
    "src/app/(auth)/register",
    "src/app/(dashboard)/dashboard",
    "src/app/(dashboard)/discovery",
    "src/app/(dashboard)/analysis",
    "src/app/(dashboard)/strategy",
    "src/app/(dashboard)/campaigns",
    "src/app/(dashboard)/analytics",
    "src/app/(dashboard)/copilot",
    "src/app/(dashboard)/settings",
    "src/components/ui",
    "src/components/layout",
    "src/components/dashboard",
    "src/lib/api",
    "src/lib/utils",
    "src/store",
    "src/types"
]

files = {
    "package.json": json.dumps({
        "name": "synexa-frontend",
        "version": "0.1.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint"
        },
        "dependencies": {
            "next": "15.0.0",
            "react": "19.0.0",
            "react-dom": "19.0.0",
            "tailwindcss": "^3.4.1",
            "framer-motion": "^11.0.0",
            "recharts": "^2.12.0",
            "zustand": "^4.5.0",
            "lucide-react": "^0.344.0",
            "clsx": "^2.1.0",
            "tailwind-merge": "^2.2.1",
            "zod": "^3.22.4",
            "react-hook-form": "^7.51.0",
            "@hookform/resolvers": "^3.3.4",
            "@tanstack/react-query": "^5.28.0",
            "@supabase/supabase-js": "^2.39.8"
        },
        "devDependencies": {
            "typescript": "^5",
            "@types/node": "^20",
            "@types/react": "^19",
            "@types/react-dom": "^19",
            "postcss": "^8",
            "eslint": "^8",
            "eslint-config-next": "15.0.0"
        }
    }, indent=2),
    "tsconfig.json": json.dumps({
        "compilerOptions": {
            "target": "es5",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "strict": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True,
            "plugins": [{"name": "next"}],
            "paths": {"@/*": ["./src/*"]}
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
        "exclude": ["node_modules"]
    }, indent=2),
    "postcss.config.js": "module.exports = { plugins: { tailwindcss: {}, autoprefixer: {} } };\n",
    "tailwind.config.ts": """import type { Config } from "tailwindcss";
const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
export default config;
""",
    "src/app/layout.tsx": """import "./globals.css";
export const metadata = { title: "Synexa Growth OS", description: "AI Executive Leadership Team" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
""",
    "src/app/globals.css": """@tailwind base;\n@tailwind components;\n@tailwind utilities;\n""",
    "src/app/page.tsx": """import { redirect } from "next/navigation";
export default function Home() {
  redirect("/dashboard");
}
""",
    "src/store/index.ts": """import { create } from 'zustand';
interface AppState { user: any; setUser: (user: any) => void; }
export const useAppStore = create<AppState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}));
""",
    "src/lib/api/client.ts": """export const apiClient = {
  get: async (url: string) => { /* TODO */ },
  post: async (url: string, data: any) => { /* TODO */ },
};
""",
}

# Generate generic page.tsx for each route
routes = [
    "src/app/(auth)/login/page.tsx",
    "src/app/(auth)/register/page.tsx",
    "src/app/(dashboard)/dashboard/page.tsx",
    "src/app/(dashboard)/discovery/page.tsx",
    "src/app/(dashboard)/analysis/page.tsx",
    "src/app/(dashboard)/strategy/page.tsx",
    "src/app/(dashboard)/campaigns/page.tsx",
    "src/app/(dashboard)/analytics/page.tsx",
    "src/app/(dashboard)/copilot/page.tsx",
    "src/app/(dashboard)/settings/page.tsx"
]

for route in routes:
    component_name = route.split("/")[-2].capitalize()
    files[route] = f"""export default function {component_name}Page() {{
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold">{component_name}</h1>
      <p className="mt-4 text-gray-600">TODO: Implement {component_name} page.</p>
    </div>
  );
}}
"""

for d in directories:
    os.makedirs(os.path.join(root_dir, d), exist_ok=True)

for path, content in files.items():
    with open(os.path.join(root_dir, path), "w") as f:
        f.write(content)

print("Frontend structure created.")
