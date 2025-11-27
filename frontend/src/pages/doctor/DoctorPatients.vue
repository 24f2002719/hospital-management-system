<template>
  <div class="card border-0 shadow-sm rounded-4">
    <div class="card-body p-4">
      
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h5 class="fw-bold mb-1">🏥 My Assigned Patients</h5>
          <p class="text-muted small mb-0">Patients you have appointments with.</p>
        </div>
        <div class="input-group w-25">
          <span class="input-group-text bg-white border-end-0">🔍</span>
          <input v-model="search" type="text" class="form-control border-start-0" placeholder="Search name...">
        </div>
      </div>
      
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>Patient Name</th>
              <th>Last Visit</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="patient in filteredPatients" :key="patient.patient_id">
              <td>
                <div class="d-flex align-items-center gap-3">
                  <div class="bg-info-subtle text-info rounded-circle d-flex align-items-center justify-content-center fw-bold" style="width: 40px; height: 40px;">
                    {{ patient.patient_name.charAt(0) }}
                  </div>
                  <span class="fw-bold text-dark">{{ patient.patient_name }}</span>
                </div>
              </td>
              
              <td class="text-secondary">
                {{ formatDate(patient.appointment_date) }}
              </td>

              <td>
                <span class="badge bg-light text-dark border">Active Patient</span>
              </td>

              <td class="text-end">
                <button 
                  class="btn btn-sm btn-outline-primary rounded-pill px-3" 
                  @click="openHistoryModal(patient)"
                >
                  📄 Medical History
                </button>
              </td>
            </tr>

            <tr v-if="filteredPatients.length === 0">
              <td colspan="4" class="text-center py-5 text-muted">
                No patients found.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="modal fade" id="historyModal" tabindex="-1" ref="modalRef">
      <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content border-0 shadow">
          
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title fw-bold">
              📂 Medical Record: {{ selectedPatientName }}
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body p-4">
            
            <div v-if="isLoading" class="text-center py-5">
              <div class="spinner-border text-primary" role="status"></div>
              <p class="text-muted mt-2">Fetching records...</p>
            </div>

            <div v-else-if="history.length === 0" class="text-center py-5 bg-light rounded-3">
              <div class="fs-1 mb-2">📋</div>
              <h6 class="fw-bold">No Records Found</h6>
              <p class="text-muted small">This patient has no completed treatments yet.</p>
            </div>

            <div v-else>
              <div v-for="record in history" :key="record.id" class="card mb-3 border-0 shadow-sm">
                <div class="card-header bg-white fw-bold d-flex justify-content-between">
                  <span>🗓️ {{ record.date }}</span>
                  <span class="text-primary">Dr. {{ record.doctor_name }}</span>
                </div>
                <div class="card-body">
                  <div class="row">
                    <div class="col-md-4 border-end">
                      <small class="text-muted fw-bold text-uppercase">Diagnosis</small>
                      <p class="mb-0 fw-medium text-dark">{{ record.diagnosis }}</p>
                    </div>
                    <div class="col-md-8">
                      <small class="text-muted fw-bold text-uppercase">Prescription</small>
                      <p class="mb-0 text-dark font-monospace bg-light p-2 rounded small">
                        {{ record.prescription }}
                      </p>
                    </div>
                  </div>
                  <div class="mt-2" v-if="record.notes">
                    <small class="text-muted fw-bold text-uppercase">Notes</small>
                    <p class="mb-0 small fst-italic text-secondary">{{ record.notes }}</p>
                  </div>
                </div>
              </div>
            </div>

          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary rounded-pill px-4" data-bs-dismiss="modal">Close</button>
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

// State
const appointments = ref([]);
const search = ref('');
const history = ref([]);
const selectedPatientName = ref('');
const isLoading = ref(false);

// Modal References
const modalRef = ref(null);
let modalInstance = null;

// --- 1. Compute Unique Patients ---
// Since we don't have a "My Patients" table in DB, we derive it from appointments
const filteredPatients = computed(() => {
  const uniqueMap = new Map();

  // Sort appointments by date desc to get latest visit first
  const sortedAppts = [...appointments.value].sort((a, b) => new Date(b.appointment_date) - new Date(a.appointment_date));

  sortedAppts.forEach(appt => {
    // Only add if not already in map AND matches search
    if (!uniqueMap.has(appt.patient_id) && appt.patient_name.toLowerCase().includes(search.value.toLowerCase())) {
      uniqueMap.set(appt.patient_id, appt);
    }
  });

  return Array.from(uniqueMap.values());
});

// --- 2. Fetch Data ---
const fetchData = async () => {
  try {
    // This returns ONLY this doctor's appointments (handled by backend logic we wrote earlier)
    const data = await api.get('/appointments');
    appointments.value = Array.isArray(data) ? data : [];
  } catch (error) {
    console.error("Error loading patients", error);
  }
};

// --- 3. View History Logic ---
const openHistoryModal = async (patient) => {
  selectedPatientName.value = patient.patient_name;
  history.value = [];
  isLoading.value = true;
  modalInstance.show();

  try {
    // We use patient_id_user (User ID) to fetch history
    const data = await api.get(`/patients/${patient.patient_id_user}/history`);
    history.value = data;
  } catch (error) {
    console.error("Failed to fetch history", error);
  } finally {
    isLoading.value = false;
  }
};

// Helper
const formatDate = (dateStr) => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
};

// Lifecycle
onMounted(() => {
  fetchData();
  modalInstance = new Modal(modalRef.value);
});
</script>