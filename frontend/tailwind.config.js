/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0D1117",
        panel: "#141B22",
        line: "#232B33",
        mist: "#8B98A5",
        signal: "#5FE0A5",
        warn: "#F2B441",
        crit: "#F2555A",
        accent: "#5B8DEF",
      },
      fontFamily: {
        mono: ["JetBrains Mono", "ui-monospace", "SFMono-Regular", "monospace"],
        sans: ["Inter", "ui-sans-serif", "system-ui"],
      },
    },
  },
  plugins: [],
};
