import { createRouter, createWebHistory } from 'vue-router'
import Watchlist from "../views/Watchlist.vue";
import Portfolio from "../views/portfolio.vue";

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
    }
  ]
})

export default router
