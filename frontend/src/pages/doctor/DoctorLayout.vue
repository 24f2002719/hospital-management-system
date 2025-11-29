<template>
  <div class="d-flex flex-column min-vh-100 bg-light">


    <div class="container py-5">
      <div class="row mb-4 align-items-center">
        <div class="col-md-6">
          <h2 class="fw-bold text-dark mb-1">Doctor Portal</h2>
          <p class="text-muted mb-0">Manage your schedule and patient treatments.</p>
        </div>
        <div class="col-md-6 text-md-end">
          <span class="badge bg-success rounded-pill px-3 py-2">👨‍⚕️ Logged in as Dr. {{ authStore.userName }}</span>
        </div>
      </div>

      <div class="card border-0 shadow-sm rounded-4 mb-4 overflow-hidden">
        <div class="card-body p-2">
          <nav class="nav nav-pills nav-fill gap-2 p-1">
            <router-link to="/doctor/dashboard" class="nav-link fw-bold rounded-pill" active-class="active shadow-sm">
              📊 Dashboard
            </router-link>
            <router-link to="/doctor/appointments" class="nav-link fw-bold rounded-pill" active-class="active shadow-sm">
              🩺 Appointments
            </router-link>
            <router-link to="/doctor/patients" class="nav-link fw-bold rounded-pill" active-class="active shadow-sm">
              🏥 My Patients
            </router-link>
            <router-link to="/doctor/availability" class="nav-link fw-bold rounded-pill" active-class="active shadow-sm">
              🕒 Availability
            </router-link>
          </nav>
        </div>
      </div>

      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>

    </div>
  </div>
</template>

<script setup>

import { useAuthStore } from '@/stores/auth';
const authStore = useAuthStore();
</script>

<style scoped>
.nav-pills .nav-link.active { background-color: #198754; color: white; } 
.nav-pills .nav-link { color: #6c757d; }
.nav-pills .nav-link:hover:not(.active) { background-color: #e9ecef; color: #198754; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>