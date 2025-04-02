/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#8E1616',
        secondary: '#D84040',
        accent: '#EEEEEE',
        neutral: '#1E3E62',
        base: '#000B58',
        danger: '#EF4444',
        warning: '#F59E0B',
        success: '#10B981',
      },
    },
  },
  plugins: [],
}