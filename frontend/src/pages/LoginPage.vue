<template>
  <div class="d-flex flex-column min-vh-100 bg-light">


    <div class="container d-flex flex-grow-1 justify-content-center align-items-center py-5">
      <div class="card border-0 shadow-lg rounded-4 overflow-hidden" style="max-width: 900px; width: 100%;">
        <div class="row g-0">
          
          <div class="col-md-6 bg-primary text-white d-flex flex-column justify-content-center align-items-center p-5 text-center">
            <div class="mb-4 display-1">🏥</div>
            <h2 class="fw-bold mb-3">Welcome Back!</h2>
            <p class="lead">
              Sign in to manage appointments, view medical records, and connect with doctors.
            </p>
          </div>

          <div class="col-md-6 bg-white p-5">
            <div class="text-center mb-4">
              <h3 class="fw-bold text-dark">Hospital Login</h3>
              <p class="text-muted">Enter your details to access your account</p>
            </div>

            <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
              {{ errorMessage }}
              <button type="button" class="btn-close" @click="errorMessage = ''"></button>
            </div>

            <form @submit.prevent="handleLogin">
              <div class="form-floating mb-3">
                <input 
                  type="email" 
                  class="form-control" 
                  id="email" 
                  v-model="email" 
                  placeholder="name@example.com" 
                  required
                >
                <label for="email" class="text-secondary">Email Address</label>
              </div>

              <div class="form-floating mb-4">
                <input 
                  type="password" 
                  class="form-control" 
                  id="password" 
                  v-model="password" 
                  placeholder="Password" 
                  required
                >
                <label for="password" class="text-secondary">Password</label>
              </div>

              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary btn-lg rounded-pill shadow-sm" :disabled="isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  <span v-if="!isLoading">Login</span>
                  <span v-else>Signing in...</span>
                </button>
              </div>
            </form>

            <div class="text-center mt-4">
              <p class="text-muted">
                Don't have an account? 
                <router-link to="/signup" class="text-primary fw-bold text-decoration-none">Sign up</router-link>
              </p>
            </div>
          </div>

        </div>
      </div>
    </div>

 
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth'; 


const router = useRouter();
const authStore = useAuthStore(); 

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const isLoading = ref(false);

const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    await authStore.login(email.value, password.value);

    if (authStore.isAdmin) {
      router.push('/admin/dashboard');
    } else if (authStore.isDoctor) {
      router.push('/doctor/dashboard'); 
    } else {
      router.push('/dashboard'); 
    }

  } catch (error) {
    errorMessage.value = error.message || "An unexpected error occurred.";
  } finally {
    isLoading.value = false;
  }
};
</script>