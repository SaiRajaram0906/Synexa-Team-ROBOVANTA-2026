import Link from 'next/link';

export default function Sidebar() {
  const links = [
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Discovery', href: '/discovery' },
    { name: 'Analysis', href: '/analysis' },
    { name: 'Strategy', href: '/strategy' },
    { name: 'Campaigns', href: '/campaigns' },
    { name: 'Analytics', href: '/analytics' },
    { name: 'AI Copilot', href: '/copilot' },
    { name: 'Settings', href: '/settings' },
  ];

  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen p-4 flex flex-col gap-2">
      {links.map((link) => (
        <Link key={link.name} href={link.href} className="p-2 hover:bg-gray-800 rounded">
          {link.name}
        </Link>
      ))}
    </aside>
  );
}
