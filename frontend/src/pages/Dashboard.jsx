import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

export default function Dashboard() {
  const [reviews, setReviews] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  const load = async (q = "") => {
    setLoading(true);
    const res = await api.get("/reviews", { params: q ? { search: q } : {} });
    setReviews(res.data.reviews);
    setLoading(false);
  };

  useEffect(() => {
    load();
  }, []);

  const onSearch = (e) => {
    e.preventDefault();
    load(search);
  };

  const remove = async (id) => {
    await api.delete(`/reviews/${id}`);
    setReviews((prev) => prev.filter((r) => r.id !== id));
  };

  return (
    <div className="mx-auto max-w-5xl px-6 py-16">
      <div className="flex items-center justify-between">
        <h1 className="font-mono text-2xl font-semibold text-white">Reviews</h1>
        <Link to="/upload" className="rounded bg-signal px-3 py-1.5 font-medium text-ink hover:bg-signal/90">
          New review
        </Link>
      </div>

      <form onSubmit={onSearch} className="mt-6 flex gap-2">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by project name…"
          className="w-full rounded border border-line bg-panel px-3 py-2 text-white outline-none focus:border-signal"
        />
        <button className="rounded border border-line px-4 py-2 text-sm hover:border-signal hover:text-signal">
          Search
        </button>
      </form>

      <div className="mt-6 flex flex-col gap-3">
        {loading && <p className="text-mist/60">Loading…</p>}
        {!loading && reviews.length === 0 && (
          <div className="rounded-lg border border-dashed border-line p-10 text-center text-mist/60">
            No reviews yet. Run your first one to see it here.
          </div>
        )}
        {reviews.map((r) => (
          <div
            key={r.id}
            className="flex items-center justify-between rounded-lg border border-line bg-panel px-5 py-4"
          >
            <Link to={`/reviews/${r.id}`} className="flex-1">
              <div className="flex items-center gap-3">
                <ScoreDial score={r.review_score} />
                <div>
                  <p className="text-sm text-white">Review #{r.id}</p>
                  <p className="font-mono text-xs text-mist/60">
                    MI {r.maintainability_index ?? "—"} · CC {r.cyclomatic_complexity ?? "—"} ·{" "}
                    {new Date(r.created_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
            </Link>
            <button
              onClick={() => remove(r.id)}
              className="rounded px-2 py-1 text-xs text-mist/50 hover:text-crit"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

function ScoreDial({ score }) {
  const color = score == null ? "text-mist/50" : score >= 80 ? "text-signal" : score >= 50 ? "text-warn" : "text-crit";
  return (
    <div className={`flex h-10 w-10 items-center justify-center rounded-full border border-line font-mono text-xs font-semibold ${color}`}>
      {score ?? "–"}
    </div>
  );
}
