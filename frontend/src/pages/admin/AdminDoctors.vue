<template>
  <div class="card border-0 shadow-sm rounded-4">
    <div class="card-body p-4">
      
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-center mb-4 gap-3">
        <div class="input-group" style="max-width: 400px;">
          <span class="input-group-text bg-white border-end-0">🔍</span>
          <input v-model="search" type="text" class="form-control border-start-0" placeholder="Search Name or Specialization...">
        </div>
        <button class="btn btn-primary rounded-pill px-4 shadow-sm" @click="openModal()">
          + Add Doctor
        </button>
      </div>

      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>Doctor Profile</th>
              <th>Specialization</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in filteredDoctors" :key="doc.id">
              <td>
                <div class="d-flex align-items-center gap-3">
                  <div class="bg-primary-subtle text-primary rounded-circle d-flex align-items-center justify-content-center fw-bold fs-5" style="width: 45px; height: 45px;">
                    {{ doc.name.charAt(0) }}
                  </div>
                  <div>
                    <h6 class="mb-0 fw-bold">{{ doc.name }}</h6>
                    <small class="text-muted">{{ doc.email }}</small>
                  </div>
                </div>
              </td>
              <td>
                <span class="badge bg-light text-dark border border-secondary-subtle">
                  {{ doc.specialization }}
                </span>
              </td>
              <td>
                <span :class="['badge', doc.active ? 'bg-success' : 'bg-secondary']">
                  {{ doc.active ? 'Active' : 'Blacklisted' }}
                </span>
              </td>
              <td class="text-end">
                <button 
                  class="btn btn-sm me-2" 
                  :class="doc.active ? 'btn-outline-warning' : 'btn-outline-success'"
                  @click="toggleStatus(doc)"
                  title="Toggle Status"
                >
                  {{ doc.active ? 'Blacklist' : 'Activate' }}
                </button>

                <button class="btn btn-sm btn-light border me-2" @click="openModal(doc)">✏️ Edit</button>
                <button class="btn btn-sm btn-light border text-danger" @click="deleteUser(doc.id)">🗑️</button>
              </td>
            </tr>
            <tr v-if="filteredDoctors.length === 0">
                <td colspan="4" class="text-center text-muted py-4">No doctors found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="modal fade" id="docModal" tabindex="-1" ref="modalRef">
      <div class="modal-dialog modal-dialog-centered modal-lg"> <div class="modal-content border-0 shadow">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title fw-bold">{{ isEdit ? 'Edit Doctor' : 'Add New Doctor' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="saveDoctor">
              
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label small fw-bold text-muted">FULL NAME</label>
                  <input v-model="form.name" class="form-control" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label small fw-bold text-muted">EMAIL</label>
                  <input v-model="form.email" type="email" class="form-control" :disabled="isEdit" required>
                </div>
              </div>

              <div class="row g-3 mt-1" v-if="!isEdit">
                <div class="col-12">
                  <label class="form-label small fw-bold text-muted">PASSWORD</label>
                  <input v-model="form.password" type="password" class="form-control" required>
                </div>
              </div>

              <div class="row g-3 mt-1">
                <div class="col-md-6">
                  <label class="form-label small fw-bold text-muted">SPECIALIZATION</label>
                  <select v-model="form.specialization" class="form-select" required>
                    <option value="" disabled>Select...</option>
                    <option v-for="s in specializations" :key="s.id" :value="s.name">{{ s.name }}</option>
                  </select>
                </div>
                
                <div class="col-md-6">
                  <label class="form-label small fw-bold text-muted">EXPERIENCE (YEARS)</label>
                  <input v-model="form.experience" type="number" min="0" class="form-control" placeholder="e.g. 5">
                </div>
              </div>

              <div class="row g-3 mt-1">
                <div class="col-12">
                   <label class="form-label small fw-bold text-muted">ADDRESS</label>
                   <input v-model="form.address" class="form-control" placeholder="Street, City">
                </div>
              </div>

              <div class="row g-3 mt-1">
                <div class="col-12">
                  <label class="form-label small fw-bold text-muted">BIO / DETAILS</label>
                  <textarea v-model="form.bio" class="form-control" rows="3" placeholder="Brief description about the doctor's background..."></textarea>
                </div>
              </div>

              <div class="d-grid mt-4">
                <button type="submit" class="btn btn-primary rounded-pill btn-lg">{{ isEdit ? 'Update Profile' : 'Create Account' }}</button>
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

const doctors = ref([]);
const specializations = ref([]);
const search = ref('');
const modalRef = ref(null);
let modalInstance = null;

const isEdit = ref(false);
const form = ref({ 
  id: null, 
  name: '', 
  email: '', 
  password: '', 
  specialization: '', 
  address: '', 
  pincode: '000000',
  experience: 0, 
  bio: '' 
});

const filteredDoctors = computed(() => {
  const q = search.value.toLowerCase();
  return doctors.value.filter(d => 
    d.name.toLowerCase().includes(q) || 
    (d.specialization && d.specialization.toLowerCase().includes(q))
  );
});

const fetchData = async () => {
  try {
    const users = await api.get('/users');
    doctors.value = users.filter(u => u.roles.includes('doctor'));
    specializations.value = await api.get('/specializations');
  } catch (e) { console.error(e); }
};

const toggleStatus = async (doc) => {
  const newStatus = !doc.active;
  const action = newStatus ? "Activate" : "Blacklist";
  
  if (!confirm(`Are you sure you want to ${action} Dr. ${doc.name}?`)) return;

  try {
    await api.put(`/users/${doc.id}`, { active: newStatus });
    doc.active = newStatus;
  } catch (error) {
    alert("Failed to update status: " + error.message);
  }
};

const openModal = (doc = null) => {
  isEdit.value = !!doc;
  if (doc) {
    form.value = { 
      ...doc, 
      password: '',
      experience: doc.experience || 0,
      bio: doc.bio || ''
    };
  } else {
    form.value = { 
      name: '', email: '', password: '', specialization: '', address: '', 
      pincode: '000000', experience: 0, bio: '' 
    };
  }
  modalInstance.show();
};

const saveDoctor = async () => {
  try {
    if (isEdit.value) await api.put(`/users/${form.value.id}`, form.value);
    else await api.post('/doctors', form.value);
    modalInstance.hide();
    fetchData();
  } catch(e) { alert(e.message); }
};

const deleteUser = async (id) => {
  if(confirm("Permanently delete this doctor? This cannot be undone.")) { 
    try {
      await api.delete(`/users/${id}`); 
      fetchData();
    } catch(e) { alert(e.message); }
  }
};

onMounted(() => {
  fetchData();
  modalInstance = new Modal(modalRef.value);
});
</script>