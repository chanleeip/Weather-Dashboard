/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html"],
  theme: {
    extend: {
      fontFamily:{
        'beabs':['Bebas Neue','cursive'],
      }
    },
  },
  plugins: [
     require('tailwindcss-bg-patterns'),
    ],
}

