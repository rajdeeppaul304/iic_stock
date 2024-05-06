/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')

module.exports = {
  content: ["./src/templates/*.html"],
  theme: {

    extend: {
      colors: {
        customBackgroundcolor: "#A5B4FC",
        customNavBGcolor: colors.gray[800],
        customNavFGcolor: "#fff",
        customNavBGHovercolor: colors.gray[700],
        customNavMobileHamcolor: colors.gray[500],
        customNavMobileHamHovercolor: colors.white,


      },
    },


  },
  plugins: [],
}
