import { defineStore } from 'pinia';
import api from '@/api';

export const useSalesStore = defineStore('sales', {
  state: () => ({
    orders: [],
    pagination: { total: 0, pages: 0, currentPage: 1 },
    loading: false
  }),
  actions: {
    async fetchSales(params = {}) {
      this.loading = true;
      try {
        const response = await api.get('/sales/', { params });
        this.orders = response.data.items;
        this.pagination = {
          total: response.data.total,
          pages: response.data.pages,
          currentPage: response.data.page
        };
      } catch (error) {
        console.error("Sales fetch failed:", error);
      } finally {
        this.loading = false;
      }
    }
  }
});