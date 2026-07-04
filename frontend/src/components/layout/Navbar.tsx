import { useAppStore } from '@/store';

export default function Navbar() {
  const user = useAppStore((state) => state.user);
  return (
    <nav className="flex items-center justify-between bg-white px-6 py-4 shadow-sm">
      <div className="font-bold text-xl text-blue-600">Synexa Growth OS</div>
      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-600">{user?.email || 'User'}</span>
        <button className="rounded bg-gray-100 px-3 py-1 text-sm hover:bg-gray-200">Logout</button>
      </div>
    </nav>
  );
}
