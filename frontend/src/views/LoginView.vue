<template>
    <div class="container d-flex align-items-center justify-content-center vh-100">
      <div class="card shadow-lg p-4" style="max-width: 400px; width: 100%;" id="card-login">
        <div class="text-center mb-4">
          <i class="bi bi-box-seam display-4 text-primary"></i>
          <h3 class="mt-2" id="login-title">Inventory Pro</h3>
        </div>
        
        <form @submit.prevent="handleSubmit" id="form-login">
          <div class="mb-3">
            <label class="form-label" for="input-username">Username</label>
            <div class="input-group">
              <span class="input-group-text"><i class="bi bi-person"></i></span>
              <input 
                v-model="form.username" 
                type="text" 
                class="form-control" 
                id="input-username" 
                required 
                placeholder="Username"
              >
            </div>
          </div>
  
          <div class="mb-3">
            <label class="form-label" for="input-password">Password</label>
            <div class="input-group">
              <span class="input-group-text"><i class="bi bi-lock"></i></span>
              <input 
                v-model="form.password" 
                type="password" 
                class="form-control" 
                id="input-password" 
                required 
                placeholder="Password"
              >
            </div>
          </div>
  
          <button 
            type="submit" 
            class="btn btn-primary w-100" 
            id="btn-login-submit" 
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2" id="login-spinner"></span>
            {{ loading ? 'Authenticating...' : 'Login' }}
          </button>
  
          <div v-if="errorMessage" class="alert alert-danger mt-3 py-2 small" id="msg-login-error">
            <i class="bi bi-exclamation-triangle-fill me-2"></i> {{ errorMessage }}
          </div>
        </form>
      </div>
    </div>
  </template>

<script setup>
import { ref, reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const auth = useAuthStore();
const router = useRouter();
const loading = ref(false);
const errorMessage = ref('');

const form = reactive({
  username: '',
  password: ''
});

const handleSubmit = async () => {
  loading.value = true;
  errorMessage.value = '';
  try {
    const success = await auth.login(form.username, form.password);
    if (success) {
      router.push('/dashboard'); // Redirect after successful login
    }
  } catch (err) {
    errorMessage.value = 'Invalid username or password. Please try again.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page { display: flex; justify-content: center; align-items: center; height: 80vh; }
.login-card { padding: 2rem; border: 1px solid #ddd; border-radius: 8px; width: 350px; }
.form-group { margin-bottom: 1rem; }
input { width: 100%; padding: 8px; margin-top: 4px; }
button { width: 100%; padding: 10px; background: #42b983; color: white; border: none; cursor: pointer; }
button:disabled { background: #ccc; }
.error { color: red; margin-top: 10px; font-size: 0.9rem; }
</style>