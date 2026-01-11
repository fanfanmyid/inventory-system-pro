import { defineStore } from 'pinia';
import api from '@/api'; // Your axios instance with the interceptor

export const useInventoryStore = defineStore('inventory', {
  state: () => ({
    products: [],
    loading: false,
  }),
  actions: {
    async fetchProducts() {
      this.loading = true;
      try {
        const response = await api.get('/products/'); // Matches your FastAPI endpoint
        this.products = response.data;
      } catch (error) {
        console.error("Failed to fetch products:", error);
      } finally {
        this.loading = false;
      }
    },
    async fetchTransactions() {
        try {
          const response = await api.get('/transactions/');
          this.transactions = response.data;
        } catch (error) {
          console.error("Failed to fetch history:", error);
        }
      }
  }
});