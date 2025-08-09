/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bolts: {
          blue: "#1e3a8a",
          green: "#22c55e",
          dark: "#0f172a",
          card: "#111827",
        }
      }
    },
  },
  plugins: [],
}
