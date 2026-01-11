import { defineStore } from 'pinia';
import api from '@/api'; // Using the axios instance we created

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') || null,
    user: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    // src/stores/auth.js
    async login(username, password) {
        try {
          // 1. Create Form Data instead of a JSON object
          const params = new URLSearchParams();
          params.append('username', username);
          params.append('password', password);
      
          // 2. Send with the correct header
          const response = await api.post('/auth/login', params, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          });
          
          this.token = response.data.access_token;
          localStorage.setItem('access_token', this.token);
          return true;
        } catch (error) {
          console.error("422 Error Detail:", error.response?.data);
          throw error;
        }

    },
    logout() {
      this.token = null;
      localStorage.removeItem('access_token');
    }
  }
});