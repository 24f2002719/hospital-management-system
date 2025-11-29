<template>
  <div class="card border-0 shadow-sm rounded-4">
    <div class="card-body p-4">
      
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-center mb-4 gap-3">
        <div class="input-group" style="max-width: 400px;">
          <span class="input-group-text bg-white border-end-0 text-muted"></span>
          <input v-model="search" type="text" class="form-control border-start-0" placeholder="Search Patient or Doctor...">
        </div>
        <div class="d-flex align-items-center gap-2">
          <label class="fw-bold text-secondary small text-nowrap">Filter by:</label>
          <select v-model="statusFilter" class="form-select rounded-pill">
            <option value="All">All Status</option>
            <option value="Booked">Booked</option>
            <option value="Completed">Completed</option>
            <option value="Cancelled">Cancelled</option>
          </select>
        </div>
      </div>

      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>Date & Time</th>
              <th>Doctor</th>
              <th>Patient</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="appt in filteredAppointments" :key="appt.id">
              <td>
                <div class="fw-bold text-dark">{{ formatDate(appt.appointment_date) }}</div>
                <div class="small text-muted">{{ appt.appointment_time }}</div>
              </td>
              <td>Dr. {{ appt.doctor_name || 'Unknown' }}</td>
              <td>
                <span class="fw-medium">{{ appt.patient_name || 'Unknown' }}</span>
              </td>
              <td>
                <span class="badge rounded-pill px-3 py-2" :class="getStatusColor(appt.status)">
                  {{ appt.status }}
                </span>
              </td>
              <td class="text-end">
                <button 
                  class="btn btn-sm btn-outline-primary rounded-pill me-2" 
                  @click="openHistoryModal(appt.patient_id_user, appt.patient_name)"
                  title="View Patient History"
                >
                  📄 History
                </button>

                <button 
                  v-if="appt.status === 'Booked'"
                  class="btn btn-sm btn-outline-danger rounded-pill px-3"
                  @click="cancelAppointment(appt.id)"
                >
                  Cancel
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="modal fade" id="historyModal" tabindex="-1" ref="historyModalRef">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-light">
            <h5 class="modal-title fw-bold">
              Patient History: <span class="text-primary">{{ selectedPatientName }}</span>
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            
            <div v-if="isLoadingHistory" class="text-center py-4">
              <div class="spinner-border text-primary" role="status"></div>
              <p class="text-muted mt-2">Loading records...</p>
            </div>

            <div v-else-if="patientHistory.length === 0" class="text-center py-4">
              <p class="text-muted">No past medical history found for this patient.</p>
            </div>

            <div v-else class="table-responsive">
              <table class="table table-bordered align-middle">
                <thead class="table-secondary">
                  <tr>
                    <th>Visit Date</th>
                    <th>Doctor</th>
                    <th>Diagnosis</th>
                    <th>Prescription</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="record in patientHistory" :key="record.id">
                    <td class="fw-bold text-nowrap">{{ record.date }}</td>
                    <td>Dr. {{ record.doctor_name }}</td>
                    <td>{{ record.diagnosis }}</td>
                    <td class="text-muted small">{{ record.prescription }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

          </div>
          <div class="modal-footer border-0">
            <button type="button" class="btn btn-secondary rounded-pill" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Modal } from 'bootstrap'; 
import api from '@/utils/api';

const appointments = ref([]);
const search = ref('');
const statusFilter = ref('All');


const historyModalRef = ref(null);
let historyModalInstance = null;
const patientHistory = ref([]);
const selectedPatientName = ref('');
const isLoadingHistory = ref(false);


const filteredAppointments = computed(() => {
  return appointments.value.filter(appt => {
    const query = search.value.toLowerCase();
    const matchesSearch = 
      (appt.doctor_name && appt.doctor_name.toLowerCase().includes(query)) ||
      (appt.patient_name && appt.patient_name.toLowerCase().includes(query));
    const matchesStatus = statusFilter.value === 'All' || appt.status === statusFilter.value;
    return matchesSearch && matchesStatus;
  });
});

const getStatusColor = (status) => {
  if (status === 'Completed') return 'bg-success-subtle text-success';
  if (status === 'Booked') return 'bg-primary-subtle text-primary';
  return 'bg-danger-subtle text-danger';
};


const fetchAppointments = async () => {
  try {
    const data = await api.get('/appointments');
    appointments.value = Array.isArray(data) ? data : [];
  } catch (error) {
    console.error("Failed to load appointments", error);
  }
};


const openHistoryModal = async (patientUserId, patientName) => {
  selectedPatientName.value = patientName;
  patientHistory.value = [];
  isLoadingHistory.value = true;
  
 
  historyModalInstance.show();

  try {
 
    const data = await api.get(`/patients/${patientUserId}/history`);
    patientHistory.value = data;
  } catch (error) {
    console.error("Failed to load history", error);
    
  } finally {
    isLoadingHistory.value = false;
  }
};

const cancelAppointment = async (id) => {
  if (!confirm("Force cancel this appointment?")) return;
  try {
    await api.delete(`/appointments/${id}`);
    const appt = appointments.value.find(a => a.id === id);
    if (appt) appt.status = 'Cancelled';
  } catch (error) {
    alert(error.message);
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
};


onMounted(() => {
  fetchAppointments();
  historyModalInstance = new Modal(historyModalRef.value);
});
</script>