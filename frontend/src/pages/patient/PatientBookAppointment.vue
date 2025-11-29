<template>
  <div class="container-fluid">
    
    <div class="card border-0 shadow-sm rounded-4 mb-5">
      <div class="card-body p-4">
        <h5 class="fw-bold mb-3">🔍 Find a Specialist</h5>
        <div class="row g-3">
          <div class="col-md-6">
            <input v-model="searchName" type="text" class="form-control form-control-lg bg-light border-0" placeholder="Search Doctor Name...">
          </div>
          <div class="col-md-6">
            <select v-model="searchSpec" class="form-select form-select-lg bg-light border-0">
              <option value="">All Departments</option>
              <option v-for="s in specializations" :key="s.id" :value="s.name">{{ s.name }}</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div v-if="filteredDoctors.length > 0" class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
      <div class="col" v-for="doc in filteredDoctors" :key="doc.id">
        <div class="card h-100 border-0 shadow-sm rounded-4 hover-card text-center position-relative overflow-hidden">
          <div class="card-body p-4 d-flex flex-column align-items-center">
            
            <div class="mb-3 position-relative">
              <div class="bg-primary-subtle text-primary rounded-circle d-inline-flex align-items-center justify-content-center fw-bold fs-2" style="width: 90px; height: 90px;">
                {{ doc.name.charAt(0) }}
              </div>
              <span class="position-absolute bottom-0 end-0 p-2 bg-success border border-light rounded-circle" title="Available"></span>
            </div>

            <h6 class="fw-bold text-dark mb-1 text-truncate w-100" :title="doc.name">{{ doc.name }}</h6>
            <span class="badge bg-light text-secondary border mb-3">{{ doc.specialization || 'General' }}</span>
            
            <div class="mt-auto w-100 d-flex flex-column gap-2">
              <button class="btn btn-sm btn-light rounded-pill fw-medium text-secondary" @click="openDetailsModal(doc)">
                View Profile
              </button>
              <button class="btn btn-outline-primary rounded-pill w-100" @click="openBookingModal(doc)">
                Book Appointment
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-5">
      <div class="fs-1 opacity-25 mb-3">👨‍⚕️</div>
      <h5 class="text-muted fw-bold">No doctors found.</h5>
      <p class="text-muted">Try adjusting your search filters.</p>
    </div>

    <div class="modal fade" id="detailsModal" tabindex="-1" ref="detailsModalRef">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow rounded-4">
          <div class="modal-body p-0">
            <div class="bg-primary p-4 text-center text-white rounded-top-4">
              <div class="bg-white text-primary rounded-circle d-inline-flex align-items-center justify-content-center fw-bold display-4 shadow mb-3" style="width: 100px; height: 100px;">
                {{ profileDoctor?.name.charAt(0) }}
              </div>
              <h4 class="fw-bold mb-1">{{ profileDoctor?.name }}</h4>
              <p class="mb-0 opacity-75">{{ profileDoctor?.specialization }} Specialist</p>
            </div>
            
            <div class="p-4">
              <h6 class="fw-bold text-muted text-uppercase small mb-2">About Doctor</h6>
              <p class="text-secondary small">
                {{ profileDoctor?.bio || 'No detailed biography available.' }}
              </p>
              
              <div class="row g-3 mt-2">
                <div class="col-6">
                  <div class="p-3 bg-light rounded-3 text-center">
                    <h5 class="fw-bold mb-0 text-primary">{{ profileDoctor?.experience || 0 }}+</h5>
                    <small class="text-muted">Years Exp.</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="p-3 bg-light rounded-3 text-center">
                    <h5 class="fw-bold mb-0 text-success">4.8</h5>
                    <small class="text-muted">Rating</small>
                  </div>
                </div>
              </div>

              <div class="d-grid mt-4 gap-2">
                <button class="btn btn-primary rounded-pill btn-lg" @click="transferToBooking(profileDoctor)">
                  Book Appointment Now
                </button>
                <button class="btn btn-link text-muted text-decoration-none" data-bs-dismiss="modal">Close</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="bookingModal" tabindex="-1" ref="bookingModalRef">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow rounded-4">
          
          <div class="modal-header bg-primary text-white">
            <div>
              <h5 class="modal-title fw-bold">Book Appointment</h5>
              <p class="mb-0 small opacity-75">with {{ selectedDoctor?.name }}</p>
            </div>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body p-4">
            <div class="mb-4">
              <label class="form-label fw-bold small text-muted">SELECT DATE</label>
              <input type="date" class="form-control form-control-lg" v-model="selectedDate" :min="minDate" @change="fetchSlots">
            </div>

            <div v-if="loadingSlots" class="text-center py-3">
              <div class="spinner-border text-primary" role="status"></div>
              <p class="text-muted mt-2 small">Checking doctor's schedule...</p>
            </div>

            <div v-else-if="selectedDate">
              <label class="form-label fw-bold small text-muted mb-2">AVAILABLE SLOTS</label>
              
              <div v-if="availableSlots.length > 0" class="d-grid grid-slots gap-2">
                <button 
                  v-for="slot in availableSlots" 
                  :key="slot"
                  class="btn btn-outline-dark rounded-3"
                  :class="{'btn-primary text-white border-primary': selectedSlot === slot}"
                  @click="selectedSlot = slot"
                >
                  {{ slot }}
                </button>
              </div>
              
              <div v-else class="alert alert-warning small text-center border-0 bg-warning-subtle text-warning-emphasis">
                <div class="fs-4 mb-2">🔒</div>
                <strong>{{ slotMessage || 'No slots available' }}</strong>
                <p class="mb-0 mt-1">The doctor is not working or fully booked on this date.</p>
              </div>
            </div>
          </div>

          <div class="modal-footer border-0 p-4 pt-0">
            <button type="button" class="btn btn-light rounded-pill px-4" data-bs-dismiss="modal">Cancel</button>
            <button 
              type="button" 
              class="btn btn-success rounded-pill px-4 fw-bold flex-grow-1" 
              :disabled="!selectedSlot || bookingLoading"
              @click="confirmBooking"
            >
              <span v-if="bookingLoading" class="spinner-border spinner-border-sm me-2"></span>
              {{ bookingLoading ? 'Confirming...' : 'Confirm Booking' }}
            </button>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { Modal } from 'bootstrap';
import api from '@/utils/api';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const doctors = ref([]);
const specializations = ref([]);
const searchName = ref('');
const searchSpec = ref('');

const bookingModalRef = ref(null);
const detailsModalRef = ref(null);
let bookingModalInstance = null;
let detailsModalInstance = null;

const selectedDoctor = ref(null);
const profileDoctor = ref(null);
const selectedDate = ref('');
const selectedSlot = ref('');
const availableSlots = ref([]);
const slotMessage = ref('');
const loadingSlots = ref(false);
const bookingLoading = ref(false);

const minDate = new Date().toISOString().split('T')[0];

const filteredDoctors = computed(() => {
  return doctors.value.filter(d => 
    d.name.toLowerCase().includes(searchName.value.toLowerCase()) &&
    (searchSpec.value === '' || d.specialization === searchSpec.value)
  );
});

const fetchData = async () => {
  try {
    specializations.value = await api.get('/specializations');
    const docsData = await api.get('/public/doctors'); 
    doctors.value = Array.isArray(docsData) ? docsData : [];
    if (route.query.spec) searchSpec.value = route.query.spec;
  } catch (e) { console.error(e); }
};

const openDetailsModal = (doc) => {
  profileDoctor.value = doc;
  detailsModalInstance.show();
};

const transferToBooking = (doc) => {
  detailsModalInstance.hide();
  openBookingModal(doc);
};

const openBookingModal = (doc) => {
  selectedDoctor.value = doc;
  selectedDate.value = '';
  selectedSlot.value = '';
  availableSlots.value = [];
  slotMessage.value = '';
  bookingModalInstance.show();
};

const fetchSlots = async () => {
  if (!selectedDate.value) return;
  
  loadingSlots.value = true;
  availableSlots.value = [];
  selectedSlot.value = '';
  slotMessage.value = '';
  
  try {
    const res = await api.get(`/doctors/${selectedDoctor.value.id}/slots?date=${selectedDate.value}`);
    
    if (res.slots && res.slots.length > 0) {
      availableSlots.value = res.slots;
    } else {
      slotMessage.value = res.message || "No slots available.";
    }
  } catch (error) {
    console.error(error);
    slotMessage.value = "Error fetching schedule.";
  } finally {
    loadingSlots.value = false;
  }
};

const confirmBooking = async () => {
  if (!selectedDate.value || !selectedSlot.value) return;
  bookingLoading.value = true;
  try {
    await api.post('/appointments', {
      doctor_id: selectedDoctor.value.id,
      date: selectedDate.value,
      time: selectedSlot.value,
      patient_user_id: authStore.user.id
    });
    bookingModalInstance.hide();
    alert("Appointment Booked Successfully! 🎉");
    router.push('/my-appointments');
  } catch (error) {
    alert("Booking Failed: " + error.message);
  } finally {
    bookingLoading.value = false;
  }
};

onMounted(() => {
  fetchData();
  bookingModalInstance = new Modal(bookingModalRef.value);
  detailsModalInstance = new Modal(detailsModalRef.value);
});
</script>

<style scoped>
.hover-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 1rem 3rem rgba(0,0,0,.075) !important;
}
.grid-slots {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
</style>