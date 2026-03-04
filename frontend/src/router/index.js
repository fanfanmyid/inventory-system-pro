import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LandingView from '../views/LandingView.vue'
import LoginView from '../views/LoginView.vue'
import SalesView from '../views/SalesView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'landing', component: LandingView },
    { path: '/login', name: 'login', component: LoginView },
    { 
      path: '/dashboard', 
      name: 'dashboard', 
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/sales',
      name: 'Sales',
      component: SalesView,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  const isLoggedIn = auth.isAuthenticated

  if (to.meta.requiresAuth && !isLoggedIn) {
    return { name: 'login' }
  }

  if (to.name === 'login' && isLoggedIn) {
    return { name: 'dashboard' }
  }

  return true
})

export default router