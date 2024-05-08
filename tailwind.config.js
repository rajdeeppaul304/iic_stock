/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')

module.exports = {
  content: ["./src/templates/*.html"],
  theme: {

    extend: {
      colors: {
        customBackgroundcolor: "#003C43",
        cardBgColor: "#77B0AA",
        FDCardBgColor: "#135D66",
        horizontalLineColor: "#000",
        FDhorizontalLinecolor: colors.blue[400],
        SectorColor: colors.red[300],
        incdecFocusColor: "#FF6347",

        // text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300
        affirmationBgColor: colors.green[700],
        affirmationBgHoverColor: colors.green[800],
        affirmationFgColor: "#fff",
        affirmationFocusRingColor: colors.green[300],

        incdecBgColor: '#135D66',
        incdecFgColor: '#E3FEF7',
        incdecBgHoverColor: '#E3FEF7',
        incdecFgHoverColor: '#135D66',

        // incdecBgColor: '#fee2bf',
        // incdecFgColor: '#6b7280',
        // incdecBgHoverColor: '#e2bffe',
        // incdecFgHoverColor: '#fff',

        incdecinputBgColor: '#135D66',
        incdecinputFgColor: '#E3FEF7',
        incdecinputFocusColor: colors.gray[400],
        incdecinputHoverColor: colors.gray[400],

        // incdecinputBgColor: '#fee2bf',
        // incdecinputFgColor: '#6b7280',
        // incdecinputHoverColor: '#000',
        // incdecinputFocusColor: '#000',

        denialBgColor: colors.red[400],
        denialBgHoverColor: colors.red[800],
        denialFgColor: "#fff",
        denialFocusRingColor: colors.red[300],

        // customNavBGcolor: colors.gray[800],
        // customNavFGcolor: "#fff",
        // customNavBGHovercolor: colors.gray[700],
        // customNavMobileHamcolor: colors.gray[500],
        // customNavMobileHamHovercolor: colors.white,

        // customNavBGcolor: "#FF7F50",
        customNavBGcolor: "#FF6347",

        // FF7F50 FF6347
        customNavFGcolor: "#fff",
        customNavBGHovercolor: colors.gray[700],
        customNavMobileHamcolor: colors.gray[500],
        customNavMobileHamHovercolor: colors.white,

        

      },
    },


  },
  plugins: [],
}
