const COLORS = {
  critical: "bg-crit/15 text-crit border-crit/40",
  high: "bg-crit/10 text-crit/90 border-crit/30",
  medium: "bg-warn/15 text-warn border-warn/40",
  low: "bg-accent/15 text-accent border-accent/40",
  info: "bg-line/40 text-mist border-line",
};

export default function SeverityBadge({ severity = "info" }) {
  const cls = COLORS[severity] || COLORS.info;
  return (
    <span className={`inline-block rounded border px-2 py-0.5 font-mono text-xs uppercase tracking-wide ${cls}`}>
      {severity}
    </span>
  );
}
