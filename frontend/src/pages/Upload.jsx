import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Upload() {
  const navigate = useNavigate();
  const [mode, setMode] = useState("file"); // 'file' | 'snippet'
  const [file, setFile] = useState(null);
  const [code, setCode] = useState("");
  const [projectName, setProjectName] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      let res;
      if (mode === "file") {
        if (!file) throw new Error("Choose a file first");
        const formData = new FormData();
        formData.append("file", file);
        res = await api.post("/upload/file", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
      } else {
        res = await api.post("/upload/snippet", { code, project_name: projectName || "Untitled snippet" });
      }
      navigate(`/reviews/${res.data.review.id}`);
    } catch (err) {
      setError(err.response?.data?.error || err.message || "Analysis failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl px-6 py-16">
      <h1 className="font-mono text-2xl font-semibold text-white">New review</h1>
      <p className="mt-1 text-sm text-mist/70">
        Upload a source file or paste a snippet. We'll run Pylint, Bandit, Radon, then an AI pass.
      </p>

      <div className="mt-6 flex gap-2 font-mono text-sm">
        <TabButton active={mode === "file"} onClick={() => setMode("file")}>
          Upload file
        </TabButton>
        <TabButton active={mode === "snippet"} onClick={() => setMode("snippet")}>
          Paste code
        </TabButton>
      </div>

      <form onSubmit={submit} className="mt-4 flex flex-col gap-4 rounded-lg border border-line bg-panel p-6">
        {mode === "file" ? (
          <label className="flex flex-col gap-2 text-sm">
            <span className="text-mist/80">Source file (.py, .js, .ts…)</span>
            <input
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              className="rounded border border-line bg-ink px-3 py-2 text-white file:mr-4 file:rounded file:border-0 file:bg-line file:px-3 file:py-1.5 file:text-mist"
            />
          </label>
        ) : (
          <>
            <label className="flex flex-col gap-2 text-sm">
              <span className="text-mist/80">Project name (optional)</span>
              <input
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="e.g. auth_helpers.py"
                className="rounded border border-line bg-ink px-3 py-2 text-white outline-none focus:border-signal"
              />
            </label>
            <label className="flex flex-col gap-2 text-sm">
              <span className="text-mist/80">Code</span>
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                rows={16}
                placeholder="Paste your code here…"
                className="rounded border border-line bg-ink px-3 py-2 font-mono text-sm text-white outline-none focus:border-signal"
              />
            </label>
          </>
        )}

        {error && <p className="font-mono text-sm text-crit">{error}</p>}

        <button
          disabled={busy}
          className="mt-2 rounded bg-signal py-2 font-medium text-ink hover:bg-signal/90 disabled:opacity-50"
        >
          {busy ? "Analyzing…" : "Run review"}
        </button>
      </form>
    </div>
  );
}

function TabButton({ active, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-t border-b-2 px-3 py-2 ${
        active ? "border-signal text-white" : "border-transparent text-mist/60 hover:text-mist"
      }`}
    >
      {children}
    </button>
  );
}
