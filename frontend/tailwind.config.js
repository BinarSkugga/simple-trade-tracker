/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,vue}",
    ],
    theme: {
        extend: {
            colors: {
                primary: '#1abc9c'
            }
        },
    },
    plugins: [

    ],
}
