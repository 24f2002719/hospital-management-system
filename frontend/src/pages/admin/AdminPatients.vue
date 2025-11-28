<template>
  <div class="card border-0 shadow-sm rounded-4">
    <div class="card-body p-4">
      
      <div class="mb-4">
        <div class="input-group" style="max-width: 400px;">
          <span class="input-group-text bg-white border-end-0">🔍</span>
          <input v-model="search" type="text" class="form-control border-start-0" placeholder="Search Patients...">
        </div>
      </div>
      
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Patient Profile</th>
              <th>Address</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in filtered" :key="p.id">
              <td><span class="text-muted small">#{{ p.id }}</span></td>
              <td>
                <div class="d-flex align-items-center gap-3">
                  <div class="bg-success-subtle text-success rounded-circle d-flex align-items-center justify-content-center fw-bold fs-5" style="width: 40px; height: 40px;">
                    {{ p.name.charAt(0) }}
                  </div>
                  <div>
                    <h6 class="mb-0 fw-bold">{{ p.name }}</h6>
                    <small class="text-muted">{{ p.email }}</small>
                  </div>
                </div>
              </td>
              <td>
                <span v-if="p.address" class="small text-secondary">{{ p.address }} - {{ p.pincode }}</span>
                <span v-else class="small text-muted">N/A</span>
              </td>
              <td>
                <span :class="['badge', p.active ? 'bg-success' : 'bg-secondary']">
                  {{ p.active ? 'Active' : 'Blacklisted' }}
                </span>
              </td>
              <td class="text-end">
                <button 
                  class="btn btn-sm me-2" 
                  :class="p.active ? 'btn-outline-warning' : 'btn-outline-success'"
                  @click="toggleStatus(p)"
                  title="Toggle Status"
                >
                  {{ p.active ? 'Blacklist' : 'Activate' }}
                </button>

                <button class="btn btn-sm btn-light border me-2" @click="openModal(p)">
                  ✏️ Edit
                </button>

                <button class="btn btn-sm btn-light border text-danger" @click="deleteUser(p.id)">
                  🗑️
                </button>
              </td>
            </tr>
            <tr v-if="filtered.length === 0">
                <td colspan="5" class="text-center text-muted py-4">No patients found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="modal fade" id="patientModal" tabindex="-1" ref="modalRef">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title fw-bold">Edit Patient</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="savePatient">
              
              <div class="mb-3">
                <label class="form-label small fw-bold text-muted">FULL NAME</label>
                <input v-model="form.name" class="form-control" required>
              </div>

              <div class="mb-3">
                <label class="form-label small fw-bold text-muted">EMAIL</label>
                <input v-model="form.email" type="email" class="form-control bg-light" disabled>
                <div class="form-text">Email cannot be changed.</div>
              </div>

              <div class="row g-2 mb-3">
                <div class="col-8">
                  <label class="form-label small fw-bold text-muted">ADDRESS</label>
                  <input v-model="form.address" class="form-control" placeholder="Street address">
                </div>
                <div class="col-4">
                  <label class="form-label small fw-bold text-muted">PINCODE</label>
                  <input v-model="form.pincode" class="form-control" placeholder="000000">
                </div>
              </div>

              <div class="mb-3" v-if="form.contact_info !== undefined">
                 <label class="form-label small fw-bold text-muted">CONTACT NUMBER</label>
                 <input v-model="form.contact_info" class="form-control" disabled>
                 <div class="form-text">Managed by patient.</div>
              </div>

              <div class="d-grid mt-4">
                <button type="submit" class="btn btn-success rounded-pill">Update Patient Profile</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

// History is uondated to reflect no changes were made here
<script setup>
import { ref, computed, onMounted } from 'vue';
import { Modal } from 'bootstrap';
import api from '@/utils/api';

const patients = ref([]);
const search = ref('');

// Modal State
const modalRef = ref(null);
let modalInstance = null;
const form = ref({ id: null, name: '', email: '', address: '', pincode: '' });

// --- Computed ---
const filtered = computed(() => patients.value.filter(p => 
  p.name.toLowerCase().includes(search.value.toLowerCase()) || 
  p.email.toLowerCase().includes(search.value.toLowerCase())
));

// --- Actions ---
const fetch = async () => {
  try {
    const users = await api.get('/users');
    patients.value = users.filter(u => u.roles.includes('patient'));
  } catch (e) { console.error(e); }
};

// Open Edit Modal
const openModal = (patient) => {
  form.value = { 
    id: patient.id, 
    name: patient.name, 
    email: patient.email, 
    address: patient.address || '', 
    pincode: patient.pincode || '',
    contact_info: patient.contact_info // Only if backend sends this
  };
  modalInstance.show();
};

// Save Changes
const savePatient = async () => {
  try {
    await api.put(`/users/${form.value.id}`, {
      name: form.value.name,
      address: form.value.address,
      pincode: form.value.pincode
    });
    
    alert("Patient updated successfully!");
    modalInstance.hide();
    fetch(); // Refresh list
  } catch (error) {
    alert(error.message || "Failed to update patient");
  }
};

const toggleStatus = async (p) => {
  const newStatus = !p.active;
  const action = newStatus ? "Activate" : "Blacklist";
  if (!confirm(`Are you sure you want to ${action} this patient?`)) return;

  try {
    await api.put(`/users/${p.id}`, { active: newStatus });
    p.active = newStatus; 
  } catch (e) { alert(e.message); }
};

const deleteUser = async (id) => {
  if(confirm("Permanently delete this patient? This cannot be undone.")) { 
    try {
      await api.delete(`/users/${id}`); 
      fetch();
    } catch(e) { alert(e.message); }
  }
};

onMounted(() => {
  fetch();
  modalInstance = new Modal(modalRef.value);
});
</script>