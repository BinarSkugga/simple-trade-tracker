/** @type {import('tailwindcss').Config} */

const Color = require('color')
const alpha = (clr, val) => Color(clr).alpha(val).rgb().string()
const lighten = (clr, val) => Color(clr).lighten(val).rgb().string()
const darken = (clr, val) => Color(clr).darken(val).rgb().string()


const primary = '#e74c3c'

module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,vue}",
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: primary,
                    lighter: lighten(primary, 1.05),
                    darker: darken(primary, 0.5)
                }
            }
        }
    },
    plugins: [],
}
