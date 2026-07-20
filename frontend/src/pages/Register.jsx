import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await register(form.name, form.email, form.password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.error || "Registration failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto flex max-w-md flex-col gap-6 px-6 py-24">
      <div>
        <h1 className="font-mono text-2xl font-semibold text-white">Create an account</h1>
        <p className="mt-1 text-sm text-mist/70">Static analysis + AI review, in one dashboard.</p>
      </div>
      <form onSubmit={submit} className="flex flex-col gap-4 rounded-lg border border-line bg-panel p-6">
        <Field label="Name" type="text" value={form.name} onChange={(v) => setForm({ ...form, name: v })} />
        <Field label="Email" type="email" value={form.email} onChange={(v) => setForm({ ...form, email: v })} />
        <Field
          label="Password"
          type="password"
          value={form.password}
          onChange={(v) => setForm({ ...form, password: v })}
        />
        {error && <p className="font-mono text-sm text-crit">{error}</p>}
        <button
          disabled={busy}
          className="mt-2 rounded bg-signal py-2 font-medium text-ink hover:bg-signal/90 disabled:opacity-50"
        >
          {busy ? "Creating account…" : "Create account"}
        </button>
      </form>
      <p className="text-center text-sm text-mist/70">
        Already have one? <Link to="/login" className="text-accent hover:underline">Sign in</Link>
      </p>
    </div>
  );
}

function Field({ label, type, value, onChange }) {
  return (
    <label className="flex flex-col gap-1 text-sm">
      <span className="text-mist/80">{label}</span>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required
        minLength={type === "password" ? 8 : undefined}
        className="rounded border border-line bg-ink px-3 py-2 text-white outline-none focus:border-signal"
      />
    </label>
  );
}
