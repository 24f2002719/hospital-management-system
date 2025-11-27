<template>
  <div class="card border-0 shadow-sm rounded-4">
    <div class="card-body p-4">
      <h5 class="fw-bold mb-4">📅 My Active Appointments</h5>
      
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light"><tr><th>Date</th><th>Doctor</th><th>Status</th><th class="text-end">Action</th></tr></thead>
          <tbody>
            <tr v-for="appt in activeAppts" :key="appt.id">
              <td>
                <div class="fw-bold">{{ formatDate(appt.appointment_date) }}</div>
                <small class="text-muted">{{ appt.appointment_time }}</small>
              </td>
              <td>Dr. {{ appt.doctor_name }}</td>
              <td><span class="badge bg-primary-subtle text-primary">{{ appt.status }}</span></td>
              <td class="text-end">
                <button class="btn btn-sm btn-outline-danger rounded-pill px-3" @click="cancelAppt(appt.id)">
                  Cancel
                </button>
              </td>
            </tr>
            <tr v-if="activeAppts.length === 0">
              <td colspan="4" class="text-center py-5 text-muted">You have no active appointments.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/utils/api';

const appointments = ref([]);

const activeAppts = computed(() => 
  appointments.value.filter(a => a.status === 'Booked')
);

const formatDate = (d) => new Date(d).toLocaleDateString('en-GB');

const fetchAppts = async () => {
  try {
    const data = await api.get('/appointments');
    appointments.value = Array.isArray(data) ? data : [];
  } catch (e) { console.error(e); }
};

const cancelAppt = async (id) => {
  if(confirm("Are you sure you want to cancel?")) {
    await api.delete(`/appointments/${id}`);
    fetchAppts();
  }
};

onMounted(fetchAppts);
</script>