<template>
  <div>
    <div class="row g-4 mb-4">
      
      <div class="col-md-4">
        <div class="card border-0 shadow-sm rounded-4 text-white bg-primary bg-gradient h-100 position-relative overflow-hidden hover-scale">
          <div class="card-body p-4 position-relative z-1">
            <h6 class="text-white-50 text-uppercase fw-bold ls-1">Total Doctors</h6>
            <div class="d-flex justify-content-between align-items-end mt-3">
              <h2 class="display-4 fw-bold mb-0">{{ stats.doctors }}</h2>
              <div class="p-2 bg-white bg-opacity-25 rounded-circle">
                <span class="fs-4">👨‍⚕️</span>
              </div>
            </div>
          </div>
          <div class="position-absolute top-0 end-0 bg-white opacity-10 rounded-circle" style="width: 150px; height: 150px; transform: translate(30%, -30%);"></div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card border-0 shadow-sm rounded-4 text-white bg-success bg-gradient h-100 position-relative overflow-hidden hover-scale">
          <div class="card-body p-4 position-relative z-1">
            <h6 class="text-white-50 text-uppercase fw-bold ls-1">Active Patients</h6>
            <div class="d-flex justify-content-between align-items-end mt-3">
              <h2 class="display-4 fw-bold mb-0">{{ stats.patients }}</h2>
              <div class="p-2 bg-white bg-opacity-25 rounded-circle">
                <span class="fs-4">🏥</span>
              </div>
            </div>
          </div>
          <div class="position-absolute top-0 end-0 bg-white opacity-10 rounded-circle" style="width: 150px; height: 150px; transform: translate(30%, -30%);"></div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card border-0 shadow-sm rounded-4 text-white bg-info bg-gradient h-100 position-relative overflow-hidden hover-scale">
          <div class="card-body p-4 position-relative z-1">
            <h6 class="text-white-50 text-uppercase fw-bold ls-1">Total Appointments</h6>
            <div class="d-flex justify-content-between align-items-end mt-3">
              <h2 class="display-4 fw-bold mb-0">{{ stats.appointments }}</h2>
              <div class="p-2 bg-white bg-opacity-25 rounded-circle">
                <span class="fs-4">📅</span>
              </div>
            </div>
          </div>
          <div class="position-absolute top-0 end-0 bg-white opacity-10 rounded-circle" style="width: 150px; height: 150px; transform: translate(30%, -30%);"></div>
        </div>
      </div>

    </div>

    <div class="row">
      <div class="col-12">
        <div class="card border-0 shadow-sm rounded-4">
          <div class="card-header bg-white py-3 border-0">
            <h5 class="fw-bold mb-0">🚀 Quick Actions</h5>
          </div>
          <div class="card-body">
            <div class="d-flex gap-3">
              <router-link to="/admin/doctors" class="btn btn-outline-primary rounded-pill px-4">
                + Add New Doctor
              </router-link>
              <router-link to="/admin/appointments" class="btn btn-outline-dark rounded-pill px-4">
                View Today's Schedule
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/utils/api';

const stats = ref({ doctors: 0, patients: 0, appointments: 0 });

onMounted(async () => {
  try {
    const users = await api.get('/users');
    const appts = await api.get('/appointments');
    
    // Filter users by role
    stats.value.doctors = users.filter(u => u.roles.includes('doctor')).length;
    stats.value.patients = users.filter(u => u.roles.includes('patient')).length;
    stats.value.appointments = Array.isArray(appts) ? appts.length : 0;
  } catch (e) {
    console.error("Failed to load stats", e);
  }
});
</script>

<style scoped>
.hover-scale { transition: transform 0.2s; }
.hover-scale:hover { transform: translateY(-5px); }
.ls-1 { letter-spacing: 1px; }
</style>