import {createRouter, createWebHistory} from 'vue-router'

const Watchlist = () => import('../views/Watchlist.vue')
const Portfolio = () => import('../views/Portfolio.vue')
const Breakdown = () => import('../views/Breakdown.vue')

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'watchlist',
            component: Watchlist
        },
        {
            path: '/portfolio',
            name: 'portfolio',
            component: Portfolio
        },
        {
            path: '/breakdown',
            name: 'breakdown',
            component: Breakdown
        }
    ]
})

export default router
