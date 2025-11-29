<template>
  <div class="card border-0 shadow-sm rounded-4">
    <div class="card-body p-4">
      <h5 class="fw-bold mb-4">📅 My Appointments</h5>
      
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>Date</th>
              <th>Doctor</th>
              <th>Status</th>
              <th>Payment</th>
              <th class="text-end">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="appt in appointments" :key="appt.id">
              <td>
                <div class="fw-bold">{{ formatDate(appt.appointment_date) }}</div>
                <small class="text-muted">{{ appt.appointment_time }}</small>
              </td>
              
              <td>Dr. {{ appt.doctor_name }}</td>
              
              <td>
                <span 
                  class="badge rounded-pill px-3"
                  :class="{
                    'bg-primary-subtle text-primary': appt.status === 'Booked',
                    'bg-success-subtle text-success': appt.status === 'Completed',
                    'bg-secondary-subtle text-secondary': appt.status === 'Cancelled'
                  }"
                >
                  {{ appt.status }}
                </span>
              </td>
              
              <td>
                <span v-if="appt.is_paid" class="badge bg-success">Paid ✅</span>
                <span v-else-if="appt.status === 'Completed'" class="badge bg-warning text-dark">Unpaid</span>
                <span v-else class="text-muted small">--</span>
              </td>

              <td class="text-end">
                <button 
                  v-if="appt.status === 'Completed' && !appt.is_paid" 
                  class="btn btn-sm btn-success rounded-pill px-3 me-2 shadow-sm"
                  @click="openPaymentModal(appt)"
                >
                  💳 Pay Now
                </button>

                <button 
                  v-if="appt.status === 'Booked'" 
                  class="btn btn-sm btn-outline-danger rounded-pill px-3" 
                  @click="cancelAppt(appt.id)"
                >
                  Cancel
                </button>
              </td>
            </tr>

            <tr v-if="appointments.length === 0">
              <td colspan="5" class="text-center py-5 text-muted">You have no appointment history.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="modal fade" id="paymentModal" tabindex="-1" ref="modalRef">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow rounded-4">
          
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title fw-bold">Secure Payment</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          
          <div class="modal-body p-4">
            <div class="text-center mb-4 bg-light p-3 rounded-3">
              <h2 class="fw-bold text-success mb-0">₹ {{ selectedAppt?.amount || 500 }}</h2>
              <p class="text-muted small mb-0">Consultation Fee</p>
            </div>

            <form @submit.prevent="processPayment">
              <div class="mb-3">
                <label class="form-label small fw-bold">CARD NUMBER</label>
                <input type="text" class="form-control" placeholder="4111 1111 1111 1111" required>
              </div>
              <div class="row">
                <div class="col-6 mb-3">
                  <label class="form-label small fw-bold">EXPIRY</label>
                  <input type="text" class="form-control" placeholder="MM/YY" required>
                </div>
                <div class="col-6 mb-3">
                  <label class="form-label small fw-bold">CVV</label>
                  <input type="password" class="form-control" placeholder="123" required>
                </div>
              </div>
              
              <div class="d-grid mt-3">
                <button type="submit" class="btn btn-success rounded-pill btn-lg" :disabled="paying">
                  <span v-if="paying" class="spinner-border spinner-border-sm me-2"></span>
                  {{ paying ? 'Processing...' : 'Pay ₹ ' + (selectedAppt?.amount || 500) }}
                </button>
              </div>
            </form>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Modal } from 'bootstrap';
import api from '@/utils/api';

const appointments = ref([]);
const modalRef = ref(null);
let modalInstance = null;

// Payment State
const selectedAppt = ref(null);
const paying = ref(false);

const formatDate = (d) => new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });

// Fetch Data
const fetchAppts = async () => {
  try {
    const data = await api.get('/appointments');
    appointments.value = Array.isArray(data) ? data.sort((a,b) => new Date(b.appointment_date) - new Date(a.appointment_date)) : [];
  } catch (e) { console.error(e); }
};

// Open Modal
const openPaymentModal = (appt) => {
  selectedAppt.value = appt;
  modalInstance.show();
};

// Process Dummy Payment
const processPayment = async () => {
  paying.value = true;
  try {
    // 1. Simulate Network Delay
    await new Promise(r => setTimeout(r, 1500));
    
    // 2. Call Backend API
    await api.post(`/pay/${selectedAppt.value.id}`, {});
    
    alert("Payment Successful! Invoice sent to email.");
    modalInstance.hide();
    
    // 3. Refresh list to update status to "Paid"
    fetchAppts(); 
  } catch (e) {
    alert("Payment Failed: " + (e.message || "Unknown error"));
  } finally {
    paying.value = false;
  }
};

const cancelAppt = async (id) => {
  if(confirm("Are you sure you want to cancel this appointment?")) {
    try {
      await api.delete(`/appointments/${id}`);
      fetchAppts();
    } catch(e) { alert(e.message); }
  }
};

onMounted(() => {
  fetchAppts();
  modalInstance = new Modal(modalRef.value);
});
</script>