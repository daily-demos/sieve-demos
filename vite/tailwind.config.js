/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "daily-gray-950": 'rgba(22, 22, 24, 1)',
        dailyGray900: 'rgba(31, 31, 34, 1)',
        dailyGray400: 'rgba(165, 168, 171, 1)',
        dailyGray50: 'rgba(250, 250, 250, 1)',
        dailyOrange: 'rgba(233, 102, 69, 1)',
        dailyOrangeHover: '#B14226',
        dailyDarkOlive: 'rgba(76, 82, 45, 1)',
        dailyDarkOliveHover: '#323A09',
        dailyDarkSkyHover: '#1D4FB7',
        dailyDarkSky: 'rgba(49, 107, 226, 1)',
      },
      fontFamily: {
        'mono': ['DM Mono']
      }
    },
  },
  plugins: [],
}