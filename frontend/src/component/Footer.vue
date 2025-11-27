<template>
  <footer class="bg-dark text-white pt-5 pb-4 mt-auto">
    <div class="container text-center text-md-start">
      <div class="row text-center text-md-start">
        
        <div class="col-md-3 col-lg-3 col-xl-3 mx-auto mt-3">
          <h5 class="text-uppercase mb-4 fw-bold text-primary">Hospital Management System</h5>
          <p>
            Providing world-class healthcare management solutions. We connect patients with the best doctors seamlessly.
          </p>
        </div>

        <div class="col-md-2 col-lg-2 col-xl-2 mx-auto mt-3">
          <h5 class="text-uppercase mb-4 fw-bold">Quick Links</h5>
          
          <template v-if="authStore.isAdmin">
            <p>
              <router-link to="/admin/dashboard" class="text-white text-decoration-none hover-link">Dashboard</router-link>
            </p>
            <p>
              <router-link to="/admin/doctors" class="text-white text-decoration-none hover-link">Manage Doctors</router-link>
            </p>
            <p>
              <router-link to="/admin/patients" class="text-white text-decoration-none hover-link">Manage Patients</router-link>
            </p>
          </template>

          <template v-else-if="authStore.isDoctor">
            <p>
              <router-link to="/doctor/dashboard" class="text-white text-decoration-none hover-link">My Dashboard</router-link>
            </p>
            <p>
              <router-link to="/doctor/appointments" class="text-white text-decoration-none hover-link">My Schedule</router-link>
            </p>
            <p>
              <router-link to="/doctor/patients" class="text-white text-decoration-none hover-link">My Patients</router-link>
            </p>
          </template>

          <template v-else-if="authStore.isPatient">
            <p>
              <router-link to="/book-appointment" class="text-white text-decoration-none hover-link">Book Appointment</router-link>
            </p>
            <p>
              <router-link to="/my-appointments" class="text-white text-decoration-none hover-link">My Appointments</router-link>
            </p>
            <p>
              <router-link to="/medical-history" class="text-white text-decoration-none hover-link">Medical History</router-link>
            </p>
          </template>

          <template v-else>
            <p>
              <router-link to="/" class="text-white text-decoration-none hover-link">Home</router-link>
            </p>
            <p>
              <router-link to="/login" class="text-white text-decoration-none hover-link">Login</router-link>
            </p>
            <p>
              <router-link to="/signup" class="text-white text-decoration-none hover-link">Sign Up</router-link>
            </p>
          </template>
        </div>

      
        
      </div>

      <hr class="mb-4">

      <div class="row align-items-center">
        <div class="col-12 text-center">
          <p class="mb-0">
            © 2025 <strong>Hospital Management System</strong>. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
const authStore = useAuthStore();
</script>

<style scoped>
.hover-link {
  transition: all 0.2s ease-in-out;
  display: inline-block;
}
.hover-link:hover {
  text-decoration: none !important;
  color: #0d6efd !important; /* Bootstrap Primary Color */
  transform: translateX(5px); /* Subtle slide effect */
}
</style>