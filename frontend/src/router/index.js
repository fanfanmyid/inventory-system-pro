import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import SalesView from '../views/SalesView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'login', component: LoginView },
    { 
      path: '/dashboard', 
      name: 'dashboard', 
      component: () => import('../views/DashboardView.vue') // Lazy load
    },
    {
      path: '/sales',
      name: 'Sales',
      component: SalesView // This connects the URL to the code we just wrote
    }
  ]
})

export default router