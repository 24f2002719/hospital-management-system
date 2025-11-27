<template>
  <div>
    <div class="row g-4 mb-4">
      <div class="col-md-4">
        <div class="card border-0 shadow-sm rounded-4 bg-primary bg-gradient text-white h-100">
          <div class="card-body p-4">
            <h6 class="text-white-50 fw-bold text-uppercase">Upcoming Bookings</h6>
            <div class="d-flex justify-content-between align-items-end mt-2">
              <h2 class="display-4 fw-bold mb-0">{{ stats.upcoming }}</h2>
              <span class="fs-1 opacity-25">📅</span>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm rounded-4 bg-success bg-gradient text-white h-100">
          <div class="card-body p-4">
            <h6 class="text-white-50 fw-bold text-uppercase">Completed Today</h6>
            <div class="d-flex justify-content-between align-items-end mt-2">
              <h2 class="display-4 fw-bold mb-0">{{ stats.completedToday }}</h2>
              <span class="fs-1 opacity-25">✅</span>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm rounded-4 bg-info bg-gradient text-white h-100">
          <div class="card-body p-4">
            <h6 class="text-white-50 fw-bold text-uppercase">Unique Patients</h6>
            <div class="d-flex justify-content-between align-items-end mt-2">
              <h2 class="display-4 fw-bold mb-0">{{ stats.totalPatients }}</h2>
              <span class="fs-1 opacity-25">👥</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-lg-8 mb-4">
        <div class="card border-0 shadow-sm rounded-4 h-100">
          <div class="card-header bg-white py-3 border-0 d-flex justify-content-between align-items-center">
            <h5 class="fw-bold mb-0">📋 Upcoming Booked Patients</h5>
            <router-link to="/doctor/appointments" class="btn btn-sm btn-outline-primary rounded-pill px-3">
              Manage All
            </router-link>
          </div>
          
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th class="ps-4">Patient Profile</th>
                  <th>Date & Time</th>
                  <th>Status</th>
                  <th class="text-end pe-4">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="appt in upcomingBooked" :key="appt.id">
                  <td class="ps-4">
                    <div class="d-flex align-items-center gap-3">
                      <div class="bg-primary-subtle text-primary rounded-circle d-flex align-items-center justify-content-center fw-bold fs-5" style="width: 45px; height: 45px;">
                        {{ appt.patient_name.charAt(0) }}
                      </div>
                      <div>
                        <h6 class="mb-0 fw-bold text-dark">{{ appt.patient_name }}</h6>
                        <small class="text-muted">ID: #{{ appt.patient_id }}</small>
                      </div>
                    </div>
                  </td>

                  <td>
                    <div class="fw-bold text-dark">{{ formatDate(appt.appointment_date) }}</div>
                    <div class="small text-muted">⏰ {{ appt.appointment_time }}</div>
                  </td>

                  <td>
                    <span class="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-2 rounded-pill">
                      ● Booked
                    </span>
                  </td>

                  <td class="text-end pe-4">
                    <router-link to="/doctor/appointments" class="btn btn-primary btn-sm rounded-pill px-3 shadow-sm">
                      Start Visit 🩺
                    </router-link>
                  </td>
                </tr>

                <tr v-if="upcomingBooked.length === 0">
                  <td colspan="4" class="text-center py-5">
                    <div class="fs-1 opacity-25 mb-3">🛌</div>
                    <h6 class="text-muted fw-bold">No upcoming bookings found.</h6>
                    <p class="text-muted small">You have no active appointments scheduled for the near future.</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="col-lg-4 mb-4">
        <div class="card border-0 shadow-sm rounded-4 bg-dark text-white h-100 overflow-hidden position-relative">
          <div class="position-absolute top-0 end-0 bg-primary opacity-25 rounded-circle" style="width: 150px; height: 150px; transform: translate(30%, -30%);"></div>
          
          <div class="card-body p-4 position-relative z-1 d-flex flex-column justify-content-center">
            <h6 class="text-white-50 text-uppercase fw-bold mb-4">🚀 Next Patient</h6>
            
            <div v-if="nextPatient" class="text-center">
              <div class="bg-white text-dark rounded-circle d-inline-flex align-items-center justify-content-center fw-bold mb-3 shadow" style="width: 80px; height: 80px; font-size: 2rem;">
                {{ nextPatient.patient_name.charAt(0) }}
              </div>
              <h3 class="fw-bold mb-1">{{ nextPatient.patient_name }}</h3>
              <p class="text-white-50 mb-4">{{ nextPatient.appointment_time }} Today</p>
              
              <router-link to="/doctor/appointments" class="btn btn-light w-100 rounded-pill fw-bold text-primary">
                Open Consultation
              </router-link>
            </div>

            <div v-else class="text-center py-4">
              <p class="text-white-50">No immediate appointments.</p>
              <router-link to="/doctor/availability" class="btn btn-outline-light btn-sm rounded-pill">
                Update Availability
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/utils/api';

const appointments = ref([]);

// --- Statistics Computed Logic ---
const stats = computed(() => {
  const todayStr = new Date().toISOString().split('T')[0];
  
  const upcomingCount = appointments.value.filter(a => a.status === 'Booked').length;
  const completedTodayCount = appointments.value.filter(a => a.status === 'Completed' && a.appointment_date === todayStr).length;
  
  // Count unique patient IDs
  const uniquePatients = new Set(appointments.value.map(a => a.patient_id)).size;

  return {
    upcoming: upcomingCount,
    completedToday: completedTodayCount,
    totalPatients: uniquePatients
  };
});

// --- List Logic: Upcoming Booked ---
const upcomingBooked = computed(() => {
  const today = new Date();
  today.setHours(0, 0, 0, 0); // Start of today

  return appointments.value
    .filter(a => {
      const apptDate = new Date(a.appointment_date);
      // Filter: Status is 'Booked' AND Date is Today or Future
      return a.status === 'Booked' && apptDate >= today;
    })
    .sort((a, b) => new Date(a.appointment_date) - new Date(b.appointment_date)) // Sort nearest first
    .slice(0, 10); // Show top 10
});

// --- Highlight: Next Patient ---
const nextPatient = computed(() => {
  const todayStr = new Date().toISOString().split('T')[0];
  // Find the first booked appointment strictly for TODAY
  return upcomingBooked.value.find(a => a.appointment_date === todayStr);
});

// --- Helper: Date Formatting ---
const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const today = new Date();
  
  // Show "Today" or "Tomorrow" for clarity
  if (date.toDateString() === today.toDateString()) return 'Today';
  
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  if (date.toDateString() === tomorrow.toDateString()) return 'Tomorrow';

  return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
};

// --- Fetch Data ---
onMounted(async () => {
  try {
    const data = await api.get('/appointments');
    appointments.value = Array.isArray(data) ? data : [];
  } catch (e) { console.error("Failed to load dashboard", e); }
});
</script>