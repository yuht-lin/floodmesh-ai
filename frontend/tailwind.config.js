/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        critical: "#ef4444",
        high: "#f97316",
        medium: "#eab308",
        low: "#3b82f6",
        darkbg: "#0f172a",
        cardbg: "#1e293b"
      }
    },
  },
  plugins: [],
}
