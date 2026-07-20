import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Home() {
  const { user } = useAuth();

  return (
    <div className="mx-auto max-w-5xl px-6 py-20">
      <div className="grid gap-12 md:grid-cols-2 md:items-center">
        <div>
          <p className="font-mono text-xs uppercase tracking-widest text-signal">static + AI review</p>
          <h1 className="mt-3 font-mono text-4xl font-semibold leading-tight text-white">
            Know what's wrong<br />before your reviewer does.
          </h1>
          <p className="mt-4 text-mist/70">
            Upload a file or paste a snippet. Pylint, Bandit, and Radon run first for
            hard metrics — then an AI pass reads the same code for bugs, smells, and
            better names.
          </p>
          <Link
            to={user ? "/upload" : "/register"}
            className="mt-6 inline-block rounded bg-signal px-5 py-2.5 font-medium text-ink hover:bg-signal/90"
          >
            {user ? "Run a review" : "Get started"}
          </Link>
        </div>

        <div className="rounded-lg border border-line bg-panel font-mono text-xs">
          <div className="flex items-center gap-1.5 border-b border-line px-4 py-2">
            <span className="h-2.5 w-2.5 rounded-full bg-crit/60" />
            <span className="h-2.5 w-2.5 rounded-full bg-warn/60" />
            <span className="h-2.5 w-2.5 rounded-full bg-signal/60" />
            <span className="ml-2 text-mist/50">auth_helpers.py</span>
          </div>
          <div className="p-4">
            <GutterLine n={12} severity="high" code="def check_password(pw, h):" note="bare except swallows all errors" />
            <GutterLine n={13} severity="medium" code="    return pw == h  # plain compare" note="use constant-time comparison" />
            <GutterLine n={14} severity="low" code="    " note="" />
            <GutterLine n={15} severity="critical" code="SECRET = 'sk_live_...'" note="hardcoded credential" />
          </div>
        </div>
      </div>
    </div>
  );
}

const DOT = {
  critical: "bg-crit",
  high: "bg-crit/70",
  medium: "bg-warn",
  low: "bg-accent",
};

function GutterLine({ n, severity, code, note }) {
  return (
    <div className="group flex items-start gap-3 py-1">
      <span className="w-5 text-right text-mist/40">{n}</span>
      <span className={`mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full ${DOT[severity] || "bg-line"}`} />
      <div className="flex-1">
        <span className="text-mist/90">{code || "\u00A0"}</span>
        {note && <p className="text-[11px] text-mist/40">{note}</p>}
      </div>
    </div>
  );
}
