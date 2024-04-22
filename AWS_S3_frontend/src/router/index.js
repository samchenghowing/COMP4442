import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../components/Home.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  }, {
    path: '/drivingSummary',
    name: 'Driving summary',
    component: () => import(/* webpackChunkName: "about" */ '../components/drivingSummary.vue')
  }, {
    path: '/speedMonitoring',
    name: 'Driving Speed monitoring',
    component: () => import(/* webpackChunkName: "about" */ '../components/speedMonitoring.vue')
  },
]

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes
})

export default router
