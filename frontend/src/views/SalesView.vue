<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
      <div class="container">
        <a class="navbar-brand" href="#" id="brand-logo"><i class="bi bi-box-seam me-2"></i>Inventory Pro</a>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link" id="nav-inventory">Inventory</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/sales" class="nav-link active" id="nav-sales">Sales</router-link>
            </li>
          </ul>
        </div>
        <button @click="logout" class="btn btn-outline-light btn-sm" id="btn-logout">
          <i class="bi bi-box-arrow-right me-2"></i>Logout
        </button>
      </div>
    </nav>
  
    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="bi bi-receipt me-2"></i>Sales History</h2>
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#newSaleModal" id="btn-open-sale-modal">
          <i class="bi bi-cart-plus me-2"></i>New Sale
        </button>
      </div>
  
      <div class="card shadow-sm border-0 mb-4 p-3 bg-light">
        <div class="row g-2">
          <div class="col-md-3">
            <input v-model="filters.invoice_number" type="text" class="form-control" placeholder="Search Invoice #..." @input="debounceSearch" id="sales-filter-invoice">
          </div>
          <div class="col-md-3">
            <input v-model="filters.product_name" type="text" class="form-control" placeholder="Search product..." @input="debounceSearch" id="sales-filter-name">
          </div>
          <div class="col-md-2">
            <input v-model="filters.start_date" type="date" class="form-control" @change="handleFilter" id="sales-filter-start">
          </div>
          <div class="col-md-2">
            <input v-model="filters.end_date" type="date" class="form-control" @change="handleFilter" id="sales-filter-end">
          </div>
          <div class="col-md-2">
            <button class="btn btn-outline-secondary w-100" @click="resetFilters" id="btn-reset-sales">
              <i class="bi bi-arrow-counterclockwise me-1"></i>Reset
            </button>
          </div>
        </div>
      </div>
  
      <div class="card shadow-sm border-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0" id="table-sales">
            <thead class="table-dark">
              <tr>
                <th width="50"></th>
                <th>Date</th>
                <th>Invoice #</th>
                <th>Items</th>
                <th>Total Amount</th>
                <th class="text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="sale in salesStore.orders" :key="sale.id">
                <tr :id="`invoice-row-${sale.id}`">
                  <td>
                    <button class="btn btn-sm btn-light border" @click="toggleRow(sale.id)">
                      <i :class="expandedRows.includes(sale.id) ? 'bi bi-chevron-up' : 'bi bi-chevron-down'"></i>
                    </button>
                  </td>
                  <td class="small">{{ new Date(sale.created_at).toLocaleString() }}</td>
                  <td class="fw-bold text-primary">{{ sale.invoice_number }}</td>
                  <td>{{ sale.items?.length || 0 }} Items</td>
                  <td class="fw-bold">Rp {{ sale.total_price.toLocaleString() }}</td>
                  <td class="text-center">
                    <button class="btn btn-sm btn-outline-info"><i class="bi bi-printer"></i></button>
                  </td>
                </tr>
                <tr v-if="expandedRows.includes(sale.id)" class="bg-light">
                  <td colspan="6" class="p-0">
                    <div class="p-3 border-start border-4 border-info">
                      <table class="table table-sm table-bordered bg-white mb-0">
                        <thead class="table-secondary">
                          <tr>
                            <th>Product Name</th>
                            <th>Qty</th>
                            <th>Unit Price</th>
                            <th>Subtotal</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="item in sale.items" :key="item.id">
                            <td>{{ item.product_name || 'Product ID: ' + item.product_id }}</td>
                            <td>{{ item.quantity }}</td>
                            <td>Rp {{ item.unit_price.toLocaleString() }}</td>
                            <td class="fw-bold">Rp {{ (item.quantity * item.unit_price).toLocaleString() }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </td>
                </tr>
              </template>
              <tr v-if="salesStore.orders.length === 0">
                <td colspan="6" class="text-center py-5 text-muted">No sales records found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  
      </div>
  </template>
  
  <script setup>
  import * as bootstrap from 'bootstrap';
  import { reactive, ref, onMounted, computed } from 'vue';
  import { useSalesStore } from '@/stores/sales';
  import { useInventoryStore } from '@/stores/inventory';
  import { useAuthStore } from '@/stores/auth';
  import { useRouter } from 'vue-router';
  import api from '@/api';
  
  const salesStore = useSalesStore();
  const inventoryStore = useInventoryStore();
  const auth = useAuthStore();
  const router = useRouter();
  
  const expandedRows = ref([]);
  const timer = ref(null);
  
  // Updated reactive filters including invoice_number
  const filters = reactive({
    invoice_number: '',
    product_name: '',
    start_date: '',
    end_date: '',
    page: 1
  });
  
  const saleForm = reactive({
    invoice_number: '',
    items: [{ product_id: null, quantity: 1, unit_price: 0 }]
  });
  
  onMounted(async () => {
    generateInvoiceNumber();
    await Promise.all([
      salesStore.fetchSales(filters),
      inventoryStore.fetchProducts()
    ]);
  });
  
  const handleFilter = () => {
    salesStore.fetchSales({
      invoice_number: filters.invoice_number || undefined,
      product_name: filters.product_name || undefined,
      start_date: filters.start_date || undefined,
      end_date: filters.end_date || undefined,
      page: filters.page
    });
  };
  
  const debounceSearch = () => {
    if (timer.value) clearTimeout(timer.value);
    timer.value = setTimeout(() => {
      filters.page = 1;
      handleFilter();
    }, 500);
  };
  
  const resetFilters = () => {
    filters.invoice_number = '';
    filters.product_name = '';
    filters.start_date = '';
    filters.end_date = '';
    filters.page = 1;
    handleFilter();
  };
  
  const generateInvoiceNumber = () => {
    saleForm.invoice_number = 'INV-' + Math.floor(Date.now() / 1000);
  };
  
  const addSaleItem = () => {
    saleForm.items.push({ product_id: null, quantity: 1, unit_price: 0 });
  };
  
  const removeSaleItem = (index) => {
    saleForm.items.splice(index, 1);
  };
  
  const updatePrice = (index) => {
    const product = inventoryStore.products.find(p => p.id === saleForm.items[index].product_id);
    // Auto-set unit price if you have price data in your product model
  };
  
  const totalAmount = computed(() => {
    return saleForm.items.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0);
  });
  
  const submitSale = async () => {
    try {
      const payload = {
        invoice_number: saleForm.invoice_number,
        items: saleForm.items,
        total_price: totalAmount.value
      };
      await api.post('/sales/', payload);
      await salesStore.fetchSales(filters);
      await inventoryStore.fetchProducts();
  
      const modal = bootstrap.Modal.getInstance(document.getElementById('newSaleModal'));
      modal.hide();
  
      generateInvoiceNumber();
      saleForm.items = [{ product_id: null, quantity: 1, unit_price: 0 }];
      alert("Sale recorded successfully!");
    } catch (err) {
      alert("Error: " + (err.response?.data?.detail || "Transaction failed"));
    }
  };
  
  const toggleRow = (id) => {
    const index = expandedRows.value.indexOf(id);
    if (index > -1) expandedRows.value.splice(index, 1);
    else expandedRows.value.push(id);
  };
  
  const logout = () => {
    auth.logout();
    router.push('/');
  };
  </script>