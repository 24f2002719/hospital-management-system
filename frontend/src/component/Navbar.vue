<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white sticky-top shadow-sm py-2">
    <div class="container">
      
      <router-link 
        class="navbar-brand fw-bold fs-4 text-primary d-flex align-items-center" 
        :to="brandLink"
      >
        Hospital Management System
      </router-link>

      <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center">
          
          <li v-if="!authStore.isAuthenticated" class="nav-item">
            <router-link class="nav-link fw-medium mx-2" to="/">Home</router-link>
          </li>
          
          <li v-if="authStore.isAdmin" class="nav-item">
             <router-link class="nav-link fw-medium mx-2 text-danger" to="/admin/dashboard">Dashboard</router-link>
          </li>

          <li v-if="authStore.isDoctor" class="nav-item">
             <router-link class="nav-link fw-medium mx-2" to="/doctor/dashboard">Dashboard</router-link>
          </li>

          <li v-if="authStore.isPatient" class="nav-item">
             <router-link class="nav-link fw-medium mx-2" to="/dashboard">Dashboard</router-link>
          </li>

          <template v-if="!authStore.isAuthenticated">
            <li class="nav-item ms-2">
              <router-link class="btn btn-outline-primary rounded-pill px-4 me-2" to="/login">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="btn btn-primary rounded-pill px-4" to="/signup">Sign Up</router-link>
            </li>
          </template>

          <li v-else class="nav-item dropdown ms-2">
            <a 
              class="nav-link dropdown-toggle fw-bold text-dark d-flex align-items-center gap-2" 
              href="#" 
              role="button" 
              @click.prevent="toggleDropdown"
              :class="{ show: isOpen }"
              aria-expanded="false"
            >
              <span>{{ authStore.userName }}</span>
              
              <span v-if="authStore.isAdmin" class="badge bg-danger" style="font-size: 0.7rem;">Admin</span>
              <span v-else-if="authStore.isDoctor" class="badge bg-success" style="font-size: 0.7rem;">Dr.</span>
              <span v-else class="badge bg-secondary" style="font-size: 0.7rem;">Patient</span>
            </a>

            <ul class="dropdown-menu dropdown-menu-end border-0 shadow" :class="{ show: isOpen }">
              <li>
                <router-link class="dropdown-item" to="/profile" @click="closeDropdown">
                  My Profile
                </router-link>
              </li>
              
              <li><hr class="dropdown-divider"></li>
              
              <li>
                <a class="dropdown-item text-danger d-flex align-items-center gap-2" href="#" @click.prevent="handleLogout">
                  <span>🚪</span> Logout
                </a>
              </li>
            </ul>
          </li>

        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth'; 

const router = useRouter();
const authStore = useAuthStore();
const isOpen = ref(false);

// --- 🟢 NEW: Logic for Brand Logo Link ---
const brandLink = computed(() => {
  if (!authStore.isAuthenticated) {
    return '/'; // Guest -> Home
  }
  // Logged In -> Go to specific dashboard
  if (authStore.isAdmin) return '/admin/dashboard';
  if (authStore.isDoctor) return '/doctor/dashboard';
  return '/dashboard'; // Patient
});

// Dropdown Logic
const toggleDropdown = () => { isOpen.value = !isOpen.value; };
const closeDropdown = () => { isOpen.value = false; };

const closeIfClickedOutside = (event) => {
  if (isOpen.value && !event.target.closest('.dropdown')) {
    isOpen.value = false;
  }
};

const handleLogout = () => {
  closeDropdown();
  authStore.logout();
  router.push('/login');
};

onMounted(() => {
  document.addEventListener('click', closeIfClickedOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', closeIfClickedOutside);
});
</script>

<style scoped>
.navbar-brand {
  letter-spacing: -0.5px;
}
.dropdown-menu.show {
  display: block;
  position: absolute;
  right: 0;
  left: auto;
}
</style>