<template>
  <div class="d-flex flex-column min-vh-100 bg-light">


    <div class="container d-flex flex-grow-1 justify-content-center align-items-center py-5">
      <div class="card border-0 shadow-lg rounded-4 overflow-hidden" style="max-width: 1000px; width: 100%;">
        <div class="row g-0">
          
          <div class="col-lg-5 bg-primary text-dark d-flex flex-column justify-content-center align-items-center p-5 text-center position-relative overflow-hidden">
            <div class="position-absolute top-0 start-0 w-100 h-100 bg-white opacity-10" style="border-radius: 50%; transform: scale(1.5) translate(-20%, -20%);"></div>
            
            <div class="position-relative z-1">
              <div class="mb-4 display-1">🚀</div>
              <h2 class="fw-bold mb-3">Join Today</h2>
              <p class="lead mb-4">
                Create an account to book appointments, access treatments, and manage your health.
              </p>
              <ul class="list-unstyled text-start mx-auto " style="max-width: 250px;">
                <li class="mb-2">- 24/7 Appointment Booking</li>
                <li class="mb-2">- Secure Medical Records</li>
                <li>- Access Top Specialists</li>
              </ul>
            </div>
          </div>

          <div class="col-lg-7 bg-white p-5">
            <h3 class="fw-bold text-dark mb-2">Create Account</h3>
            <p class="text-muted mb-4">Fill in your details to get started.</p>

            <div v-if="apiError" class="alert alert-danger alert-dismissible fade show" role="alert">
              {{ apiError }}
              <button type="button" class="btn-close" @click="apiError = ''"></button>
            </div>

            <div v-if="successMessage" class="alert alert-success" role="alert">
              {{ successMessage }} Redirecting to login...
            </div>

            <form @submit.prevent="handleSignup" novalidate v-if="!successMessage">
              
              <div class="row g-3 mb-3">
                <div class="col-md-6">
                  <div class="form-floating">
                    <input 
                      type="text" 
                      class="form-control" 
                      id="name" 
                      v-model="form.name" 
                      :class="{ 'is-invalid': errors.name }" 
                      placeholder="Name"
                    >
                    <label for="name">Full Name</label>
                    <div class="invalid-feedback">{{ errors.name }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-floating">
                    <input 
                      type="email" 
                      class="form-control" 
                      id="email" 
                      v-model="form.email" 
                      :class="{ 'is-invalid': errors.email }" 
                      placeholder="name@example.com"
                    >
                    <label for="email">Email Address</label>
                    <div class="invalid-feedback">{{ errors.email }}</div>
                  </div>
                </div>
              </div>

              <div class="row g-3 mb-3">
                <div class="col-md-6">
                  <div class="form-floating">
                    <input 
                      type="password" 
                      class="form-control" 
                      id="password" 
                      v-model="form.password" 
                      :class="{ 'is-invalid': errors.password }" 
                      placeholder="Password"
                    >
                    <label for="password">Password</label>
                    <div class="invalid-feedback">{{ errors.password }}</div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-floating">
                    <input 
                      type="password" 
                      class="form-control" 
                      id="confirmPassword" 
                      v-model="form.confirmPassword" 
                      :class="{ 'is-invalid': errors.confirmPassword }" 
                      placeholder="Confirm Password"
                    >
                    <label for="confirmPassword">Confirm Password</label>
                    <div class="invalid-feedback">{{ errors.confirmPassword }}</div>
                  </div>
                </div>
              </div>

              <div class="row g-3 mb-4">
                <div class="col-md-8">
                  <div class="form-floating">
                    <input 
                      type="text" 
                      class="form-control" 
                      id="address" 
                      v-model="form.address" 
                      placeholder="123 Main St"
                    >
                    <label for="address">Address (Optional)</label>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="form-floating">
                    <input 
                      type="text" 
                      class="form-control" 
                      id="pincode" 
                      v-model="form.pincode" 
                      placeholder="10001"
                    >
                    <label for="pincode">Pincode</label>
                  </div>
                </div>
              </div>

              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary btn-lg rounded-pill shadow-sm" :disabled="isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  <span v-if="!isLoading">Create Account</span>
                  <span v-else>Registering...</span>
                </button>
              </div>
            </form>

            <div class="text-center mt-4">
              <p class="text-muted">
                Already have an account? 
                <router-link to="/login" class="text-primary fw-bold text-decoration-none">Log in</router-link>
              </p>
            </div>

          </div>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  address: '',
  pincode: ''
});

const errors = reactive({});
const apiError = ref('');
const successMessage = ref('');
const isLoading = ref(false);

const validate = () => {
  Object.keys(errors).forEach(key => delete errors[key]);

  let isValid = true;

  if (!form.name.trim()) {
    errors.name = 'Full name is required';
    isValid = false;
  }

  const emailPattern = /^\S+@\S+\.\S+$/;
  if (!form.email.trim()) {
    errors.email = 'Email is required';
    isValid = false;
  } else if (!emailPattern.test(form.email)) {
    errors.email = 'Please enter a valid email';
    isValid = false;
  }

  if (!form.password) {
    errors.password = 'Password is required';
    isValid = false;
  } else if (form.password.length < 6) {
    errors.password = 'Password must be at least 6 characters';
    isValid = false;
  }

  if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match';
    isValid = false;
  }

  return isValid;
};

const handleSignup = async () => {
  if (!validate()) return;

  isLoading.value = true;
  apiError.value = '';

  try {
    const response = await fetch('http://127.0.0.1:5000/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: form.name,
        email: form.email,
        password: form.password,
        address: form.address,
        pincode: form.pincode
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || data.error || 'Registration failed');
    }

    successMessage.value = 'Account created successfully!';
    
    setTimeout(() => {
      router.push('/login');
    }, 2000);

  } catch (error) {
    apiError.value = error.message;
  } finally {
    isLoading.value = false;
  }
};
</script>