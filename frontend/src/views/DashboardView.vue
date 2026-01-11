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
            <router-link to="/sales" class="nav-link" id="nav-sales">Sales</router-link>
            </li>
        </ul>
        </div>

        <button @click="logout" class="btn btn-outline-light btn-sm" id="btn-logout">
        <i class="bi bi-box-arrow-right me-2"></i>Logout
        </button>
    </div>
    </nav>
  
    <div class="container">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2><i class="bi bi-list-ul me-2"></i>Product List</h2>
        <button class="btn btn-success" id="btn-add-product"><i class="bi bi-plus-circle me-2"></i>Add Product</button>
      </div>
  
      <div class="card shadow-sm">
        <div v-if="successMessage" class="alert alert-success alert-dismissible fade show shadow-sm m-3" id="msg-success-tx" role="alert">
          <i class="bi bi-check-circle-fill me-2"></i>
          <strong>Success!</strong> {{ successMessage }}
          <button type="button" class="btn-close" @click="successMessage = ''" aria-label="Close"></button>
        </div>
  
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0" id="table-inventory">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Product Name</th>
                <th>SKU</th>
                <th>Stock</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in inventory.products" :key="product.id" :id="`row-product-${product.id}`">
                <td>#{{ product.id }}</td>
                <td class="fw-bold">{{ product.name }}</td>
                <td><span class="badge bg-secondary">{{ product.sku }}</span></td>
                <td>
                  <span :id="`stock-val-${product.id}`" :class="['badge', product.stock < 5 ? 'bg-danger' : 'bg-primary']">
                    {{ product.stock }} units
                  </span>
                </td>
                <td class="text-center">
                  <button 
                    class="btn btn-sm btn-info text-white" 
                    :id="`btn-update-stock-${product.id}`"
                    data-bs-toggle="modal" 
                    data-bs-target="#transactionModal"
                    @click="prepareTransaction(product)"
                  >
                    <i class="bi bi-arrow-left-right"></i> Update Stock
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  
      <div class="mt-5 mb-5">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h2><i class="bi bi-clock-history me-2"></i>Transaction History</h2>
          <button class="btn btn-outline-secondary btn-sm" id="btn-refresh-history" @click="inventory.fetchTransactions">
            <i class="bi bi-arrow-clockwise"></i> Refresh
          </button>
        </div>
  
        <div class="card shadow-sm">
          <div class="table-responsive">
            <table class="table table-sm table-striped align-middle mb-0" id="table-history">
              <thead class="table-dark">
                <tr>
                  <th>Date & Time</th>
                  <th>Product</th>
                  <th>Type</th>
                  <th>Quantity</th>
                  <th>Reference</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="tx in inventory.transactions" :key="tx.id" :id="`row-tx-${tx.id}`">
                  <td class="small text-muted">{{ new Date(tx.created_at).toLocaleString() }}</td>
                  <td class="fw-bold">{{ tx.product_name || 'Product #' + tx.product_id }}</td>
                  <td>
                    <span :class="['badge', tx.transaction_type === 'IN' ? 'bg-success' : 'bg-warning text-dark']">
                      {{ tx.transaction_type }}
                    </span>
                  </td>
                  <td :class="tx.transaction_type === 'IN' ? 'text-success' : 'text-danger'">
                    {{ tx.transaction_type === 'IN' ? '+' : '-' }}{{ tx.quantity }}
                  </td>
                  <td class="text-muted small">{{ tx.reference }}</td>
                </tr>
                <tr v-if="!inventory.transactions || inventory.transactions.length === 0">
                  <td colspan="5" class="text-center py-4 text-muted">No transactions found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  
    <div class="modal fade" id="transactionModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="modal-title">Update Stock: {{ selectedProduct?.name }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="btn-close-modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitTransaction">
              <div class="mb-3">
                <label class="form-label">Transaction Type</label>
                <select class="form-select" v-model="form.transaction_type" id="select-type" required>
                  <option value="IN">Stock IN (Restock)</option>
                  <option value="OUT">Stock OUT (Sale)</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Quantity</label>
                <input type="number" class="form-control" v-model.number="form.quantity" id="input-quantity" min="1" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Reference Note</label>
                <input type="text" class="form-control" v-model="form.reference" id="input-reference" placeholder="e.g. Monthly restock">
              </div>
              <div class="modal-footer px-0 pb-0">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="btn-cancel-tx">Cancel</button>
                <button type="submit" class="btn btn-primary" id="btn-submit-tx">Submit Transaction</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import * as bootstrap from 'bootstrap'; // Crucial for modal control
  import { onMounted, reactive, ref } from 'vue';
  import { useInventoryStore } from '@/stores/inventory';
  import { useAuthStore } from '@/stores/auth';
  import { useRouter } from 'vue-router';
  import api from '@/api';
  
  const inventory = useInventoryStore();
  const auth = useAuthStore();
  const router = useRouter();
  
  const selectedProduct = ref(null);
  const successMessage = ref('');
  const form = reactive({
    transaction_type: 'IN',
    quantity: 1,
    reference: ''
  });
  
  // Cleaned up onMounted
  onMounted(async () => {
    await inventory.fetchProducts();
    await inventory.fetchTransactions();
  });
  
  const prepareTransaction = (product) => {
    selectedProduct.value = product;
  };
  
  const submitTransaction = async () => {
    try {
      const payload = {
        product_id: selectedProduct.value.id,
        quantity: form.quantity,
        transaction_type: form.transaction_type,
        reference: form.reference || "Manual Adjustment"
      };
  
      // API calls
      await api.post('/transactions/', payload);
      await inventory.fetchProducts();
      await inventory.fetchTransactions();
  
      // Show success UI
      successMessage.value = `Successfully updated stock for ${selectedProduct.value.name}!`;
      setTimeout(() => { successMessage.value = ''; }, 3000);
  
      // Bootstrap Modal Cleanup
      const modalElement = document.getElementById('transactionModal');
      if (modalElement) {
        const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);
        modalInstance.hide();
        
        // Safety net to remove stuck backdrops
        document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());
        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
      }
  
      // Reset Form
      form.quantity = 1;
      form.reference = '';
      
    } catch (err) {
      console.error("Submission Error:", err);
      alert(`Error: ${err.response?.data?.detail || "Transaction failed"}`);
    }
  };
  
  const logout = () => {
    auth.logout();
    router.push('/');
  };
  </script>