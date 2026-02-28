import { defineStore } from 'pinia';
import api from '@/api';

export const useInventoryStore = defineStore('inventory', {
  state: () => ({
    transactions: [],
    pagination: {
      total: 0,
      pages: 0,
      currentPage: 1
    },
    loading: false
  }),

  actions: {
    async fetchTransactions(params = {}) {
      this.loading = true;
      try {
        // params will include product_name, start_date, end_date, page, size
        const response = await api.get('/transactions/', { params });
        
        // Match the structure we built in the backend
        this.transactions = response.data.items;
        this.pagination = {
          total: response.data.total,
          pages: response.data.pages,
          currentPage: response.data.page
        };
      } catch (error) {
        console.error("Error fetching transactions:", error);
      } finally {
        this.loading = false;
      }
    },
    async fetchProducts() {
        try {
          const response = await api.get('/products/');
          // Ensure you are assigning the data correctly
          this.products = response.data; 
        } catch (error) {
          console.error("Products error:", error);
          this.products = []; // Keep it as an array to avoid .length errors
        }
      }
  }
});