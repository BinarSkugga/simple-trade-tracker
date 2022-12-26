/** @type {import('tailwindcss').Config} */

const Color = require('color')
const alpha = (clr, val) => Color(clr).alpha(val).rgb().string()
const lighten = (clr, val) => Color(clr).lighten(val).rgb().string()
const darken = (clr, val) => Color(clr).darken(val).rgb().string()

module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,vue}",
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: '#1abc9c',
                    lighter: lighten('#1abc9c', 1.05),
                    darker: darken('#1abc9c', 0.5)
                }
            }
        }
    },
    plugins: [],
}
