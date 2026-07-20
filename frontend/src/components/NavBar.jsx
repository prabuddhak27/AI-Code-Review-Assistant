import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function NavBar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <header className="border-b border-line bg-panel/60 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link to="/" className="flex items-baseline gap-2 font-mono text-lg font-semibold text-white">
          <span className="text-signal">&gt;_</span>
          codelint
        </Link>
        <nav className="flex items-center gap-6 text-sm">
          {user ? (
            <>
              <Link to="/dashboard" className="hover:text-white">Dashboard</Link>
              <Link to="/upload" className="hover:text-white">New review</Link>
              <span className="text-mist/60">{user.name}</span>
              <button
                onClick={() => { logout(); navigate("/login"); }}
                className="rounded border border-line px-3 py-1.5 hover:border-crit hover:text-crit"
              >
                Sign out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="hover:text-white">Sign in</Link>
              <Link
                to="/register"
                className="rounded bg-signal px-3 py-1.5 font-medium text-ink hover:bg-signal/90"
              >
                Get started
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
