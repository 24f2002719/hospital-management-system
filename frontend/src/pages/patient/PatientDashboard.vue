<template>
  <div>
    <div class="row g-4 mb-4">
      <div class="col-md-8">
        <div class="card border-0 shadow-sm rounded-4 h-100 bg-primary bg-gradient text-white overflow-hidden position-relative">
          <div class="card-body p-4 position-relative z-1">
            <h4 class="fw-bold">Need a checkup?</h4>
            <p class="mb-4 text-white-50">Find the best specialists near you and book an appointment in seconds.</p>
            <router-link to="/book-appointment" class="btn btn-light rounded-pill px-4 fw-bold text-primary">
              Book Appointment Now
            </router-link>
          </div>
          <div class="position-absolute bottom-0 end-0 opacity-25" style="font-size: 8rem; line-height: 0.8; margin-right: -20px;">🩺</div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm rounded-4 h-100 bg-white">
          <div class="card-body p-4 text-center d-flex flex-column justify-content-center">
            <h6 class="text-uppercase text-muted fw-bold small">Upcoming</h6>
            <h2 class="display-4 fw-bold text-dark mb-0">{{ upcomingCount }}</h2>
            <p class="text-muted small">Active Appointments</p>
          </div>
        </div>
      </div>
    </div>

    <h5 class="fw-bold mb-3">🏥 Departments</h5>
    <div class="row g-3 mb-5">
      <div class="col-6 col-md-3" v-for="spec in specializations" :key="spec.id">
        <div 
          class="card border-0 shadow-sm rounded-4 h-100 hover-card cursor-pointer" 
          @click="goToBooking(spec.name)"
        >
          <div class="card-body text-center p-3">
            <div class="bg-primary-subtle text-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-2" style="width: 50px; height: 50px; font-size: 1.5rem;">
              {{ getIcon(spec.name) }}
            </div>
            <h6 class="fw-bold mb-1">{{ spec.name }}</h6>
            <div class="d-flex align-items-center justify-content-center gap-1 text-primary small fw-bold mt-2">
              <span>Book Now</span>
              <span>➜</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card border-0 shadow-sm rounded-4">
      <div class="card-header bg-white py-3 border-0 d-flex justify-content-between align-items-center">
        <h5 class="fw-bold mb-0">📅 Upcoming Schedule</h5>
        <router-link to="/my-appointments" class="btn btn-sm btn-outline-primary rounded-pill">View All</router-link>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light"><tr><th>Date</th><th>Doctor</th><th>Status</th></tr></thead>
            <tbody>
              <tr v-for="appt in upcomingAppts" :key="appt.id">
                <td class="fw-bold">{{ formatDate(appt.appointment_date) }} <small class="text-muted ms-1">{{ appt.appointment_time }}</small></td>
                <td>Dr. {{ appt.doctor_name }}</td>
                <td><span class="badge bg-primary-subtle text-primary">Booked</span></td>
              </tr>
              <tr v-if="upcomingAppts.length === 0">
                <td colspan="3" class="text-center py-4 text-muted">No upcoming appointments.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router'; // Import Router
import api from '@/utils/api';

const router = useRouter();
const specializations = ref([]);
const appointments = ref([]);

const upcomingAppts = computed(() => 
  appointments.value.filter(a => a.status === 'Booked').slice(0, 3)
);

const upcomingCount = computed(() => 
  appointments.value.filter(a => a.status === 'Booked').length
);

const formatDate = (d) => new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });

const getIcon = (name) => {
  const map = { 'Cardiology': '❤️', 'Neurology': '🧠', 'Pediatrics': '👶', 'Orthopedics': '🦴', 'Dermatology': '✨', 'General Surgery': '🏥' };
  return map[name] || '⚕️';
};

// Navigation Function
const goToBooking = (specName) => {
  router.push({ path: '/book-appointment', query: { spec: specName } });
};

onMounted(async () => {
  try {
    specializations.value = await api.get('/specializations');
    appointments.value = await api.get('/appointments');
  } catch (e) { console.error(e); }
});
</script>

<style scoped>
.hover-card { 
  transition: transform 0.2s ease, box-shadow 0.2s ease; 
  cursor: pointer; 
}
.hover-card:hover { 
  transform: translateY(-5px); 
  box-shadow: 0 .5rem 1rem rgba(0,0,0,.15)!important; 
}
</style>