/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // scan all JS/TS files in src
    "./public/index.html",        // also scan your main HTML
  ],
  theme: {
    extend: {
      fontFamily: {
        titillium: ['Titillium Web', 'sans-serif'],  // your custom font family
      },
    },
  },
  plugins: [],
};
