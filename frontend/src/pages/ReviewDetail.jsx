import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";
import SeverityBadge from "../components/SeverityBadge";

export default function ReviewDetail() {
  const { id } = useParams();
  const [review, setReview] = useState(null);

  useEffect(() => {
    api.get(`/reviews/${id}`).then((res) => setReview(res.data.review));
  }, [id]);

  const downloadMarkdown = () => {
    window.open(`/api/reports/${id}/markdown`, "_blank");
  };

  if (!review) return <div className="px-6 py-16 text-mist/60">Loading…</div>;

  return (
    <div className="mx-auto max-w-4xl px-6 py-16">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="font-mono text-2xl font-semibold text-white">Review #{review.id}</h1>
          <p className="mt-2 max-w-xl text-sm text-mist/70">{review.summary}</p>
        </div>
        <button
          onClick={downloadMarkdown}
          className="rounded border border-line px-3 py-1.5 text-sm hover:border-signal hover:text-signal"
        >
          Export .md
        </button>
      </div>

      <div className="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-4">
        <Metric label="Score" value={review.review_score ?? "—"} />
        <Metric label="Maintainability" value={review.maintainability_index ?? "—"} />
        <Metric label="Avg complexity" value={review.cyclomatic_complexity ?? "—"} />
        <Metric label="Lines of code" value={review.lines_of_code ?? "—"} />
      </div>

      <h2 className="mt-10 font-mono text-lg text-white">Findings</h2>
      <div className="mt-4 flex flex-col gap-2">
        {review.findings.length === 0 && (
          <p className="text-sm text-mist/60">No findings — clean pass.</p>
        )}
        {review.findings.map((f) => (
          <div
            key={f.id}
            className={`severity-${f.severity} rounded bg-panel px-4 py-3`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <SeverityBadge severity={f.severity} />
                <span className="font-mono text-xs uppercase text-mist/50">{f.source}</span>
                {f.line_number && (
                  <span className="font-mono text-xs text-mist/50">line {f.line_number}</span>
                )}
              </div>
            </div>
            <p className="mt-2 text-sm font-medium text-white">{f.issue}</p>
            {f.explanation && <p className="mt-1 text-sm text-mist/70">{f.explanation}</p>}
            {f.suggestion && (
              <p className="mt-1 text-sm text-signal/90">Suggestion: {f.suggestion}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div className="rounded-lg border border-line bg-panel px-4 py-3">
      <p className="font-mono text-xl font-semibold text-white">{value}</p>
      <p className="text-xs text-mist/60">{label}</p>
    </div>
  );
}
