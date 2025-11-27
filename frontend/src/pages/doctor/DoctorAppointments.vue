<template>
  <div class="card border-0 shadow-sm rounded-4">
    <div class="card-body p-4">
      
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h5 class="fw-bold mb-0">🩺 My Appointment Schedule</h5>
        <div class="input-group w-50">
          <span class="input-group-text bg-white border-end-0">🔍</span>
          <input v-model="search" type="text" class="form-control border-start-0" placeholder="Search Patient Name...">
        </div>
      </div>

      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>Date / Time</th>
              <th>Patient Details</th>
              <th>Status</th>
              <th class="text-end">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="appt in filteredAppointments" :key="appt.id">
              <td>
                <div class="fw-bold text-dark">{{ formatDate(appt.appointment_date) }}</div>
                <div class="small text-muted">{{ appt.appointment_time }}</div>
              </td>
              
              <td>
                <span class="fw-bold text-primary">{{ appt.patient_name }}</span>
              </td>

              <td>
                <span 
                  class="badge rounded-pill px-3"
                  :class="{
                    'bg-primary': appt.status === 'Booked',
                    'bg-success': appt.status === 'Completed',
                    'bg-secondary': appt.status === 'Cancelled'
                  }"
                >
                  {{ appt.status }}
                </span>
              </td>

              <td class="text-end">
                <button 
                  v-if="appt.status === 'Booked'" 
                  class="btn btn-sm btn-success rounded-pill px-3 me-2"
                  @click="openConsultationModal(appt)"
                >
                  📝 Consult / Update History
                </button>

                <button 
                  v-if="appt.status === 'Booked'"
                  class="btn btn-sm btn-outline-danger rounded-circle"
                  @click="cancelAppt(appt.id)"
                  title="Cancel Appointment"
                >
                  ✕
                </button>

                <button 
                  v-if="appt.status === 'Completed'" 
                  class="btn btn-sm btn-light border rounded-pill"
                  disabled
                >
                  ✅ Done
                </button>
              </td>
            </tr>
            <tr v-if="filteredAppointments.length === 0">
              <td colspan="4" class="text-center py-4 text-muted">No appointments found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="modal fade" id="consultModal" tabindex="-1" ref="modalRef">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title fw-bold">Update Patient History</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            
            <div class="alert alert-light border mb-3">
              <strong>Patient:</strong> {{ selectedAppt?.patient_name }} <br>
              <strong>Date:</strong> {{ formatDate(selectedAppt?.appointment_date) }} at {{ selectedAppt?.appointment_time }}
            </div>

            <form @submit.prevent="saveHistory">
              <div class="mb-3">
                <label class="form-label fw-bold">Diagnosis</label>
                <textarea 
                  v-model="form.diagnosis" 
                  class="form-control" 
                  rows="2" 
                  placeholder="e.g. Acute Bronchitis, Viral Fever..." 
                  required
                ></textarea>
              </div>

              <div class="mb-3">
                <label class="form-label fw-bold">Prescription</label>
                <div class="row g-2">
                  <div class="col-12">
                    <textarea 
                      v-model="form.prescription" 
                      class="form-control font-monospace" 
                      rows="4" 
                      placeholder="Rx:&#10;1. Tab Paracetamol 500mg - BD x 3 days&#10;2. Syp Cough Syrup - 10ml HS"
                    ></textarea>
                  </div>
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label fw-bold">Additional Notes</label>
                <input 
                  v-model="form.notes" 
                  class="form-control" 
                  placeholder="e.g. Patient advised to rest for 2 days"
                >
              </div>

              <div class="d-grid gap-2 d-md-flex justify-content-md-end mt-4">
                <button type="button" class="btn btn-light rounded-pill px-4" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary rounded-pill px-4">Save & Complete</button>
              </div>
            </form>

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
const modalRef = ref(null);
let modalInstance = null;

const selectedAppt = ref(null);
const form = ref({ diagnosis: '', prescription: '', notes: '' });

// Filter logic: Search by Patient Name
const filteredAppointments = computed(() => 
  appointments.value.filter(a => a.patient_name.toLowerCase().includes(search.value.toLowerCase()))
);

const fetchData = async () => {
  try {
    // Backend now filters this automatically based on logged-in Doctor ID
    const data = await api.get('/appointments');
    appointments.value = Array.isArray(data) ? data : [];
  } catch (e) { console.error(e); }
};

const openConsultationModal = (appt) => {
  selectedAppt.value = appt;
  form.value = { diagnosis: '', prescription: '', notes: '' };
  modalInstance.show();
};

const saveHistory = async () => {
  try {
    // 1. Create Treatment (This updates the history)
    await api.post('/treatments', {
      appointment_id: selectedAppt.value.id,
      diagnosis: form.value.diagnosis,
      prescription: form.value.prescription,
      notes: form.value.notes
    });

    // 2. Mark Appointment as Completed
    await api.put(`/appointments/${selectedAppt.value.id}`, { status: 'Completed' });

    alert("Patient history updated successfully!");
    modalInstance.hide();
    fetchData(); // Refresh list
  } catch (e) {
    alert("Error saving: " + e.message);
  }
};

const cancelAppt = async (id) => {
  if(!confirm("Are you sure you want to cancel this appointment?")) return;
  try {
    await api.delete(`/appointments/${id}`); // Or update status to 'Cancelled'
    fetchData();
  } catch(e) { alert(e.message); }
};

const formatDate = (d) => {
  if(!d) return '';
  return new Date(d).toLocaleDateString('en-GB');
};

onMounted(() => {
  fetchData();
  modalInstance = new Modal(modalRef.value);
});
</script>