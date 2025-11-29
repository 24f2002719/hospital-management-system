<template>
  <div class="card border-0 shadow-sm rounded-4">
    <div class="card-body p-4">
      
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-center mb-4 gap-3">
        <h5 class="fw-bold mb-0">📂 Medical History</h5>
        
        <button 
          class="btn btn-outline-primary rounded-pill px-4 shadow-sm" 
          @click="exportData" 
          :disabled="exportLoading || history.length === 0"
        >
          <span v-if="exportLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
          {{ exportLoading ? 'Sending Email...' : '📥 Email CSV Report' }}
        </button>
      </div>
      
      <div v-if="history.length === 0" class="text-center py-5">
        <div class="fs-1 opacity-25 mb-3">📄</div>
        <p class="text-muted fw-bold">No past medical records found.</p>
        <p class="text-muted small">Once you complete an appointment, your diagnosis will appear here.</p>
      </div>

      <div v-else class="accordion" id="historyAccordion">
        <div class="accordion-item border-0 mb-3 shadow-sm rounded overflow-hidden" v-for="(record, index) in history" :key="record.id">
          
          <h2 class="accordion-header">
            <button class="accordion-button collapsed fw-bold bg-white" type="button" data-bs-toggle="collapse" :data-bs-target="'#c'+index">
              <span class="text-primary me-2">🗓️ {{ record.date }}</span> 
              <span class="text-dark"> — Dr. {{ record.doctor_name }}</span>
            </button>
          </h2>
          
          <div :id="'c'+index" class="accordion-collapse collapse" data-bs-parent="#historyAccordion">
            <div class="accordion-body bg-light">
              <div class="row">
                
                <div class="col-md-12 mb-3">
                  <label class="small fw-bold text-secondary text-uppercase ls-1">Diagnosis</label>
                  <p class="fw-medium text-dark mt-1">{{ record.diagnosis }}</p>
                </div>
                
                <div class="col-md-12">
                  <label class="small fw-bold text-secondary text-uppercase ls-1">Prescription</label>
                  <div class="bg-white p-3 rounded border border-light-subtle font-monospace mt-1 shadow-sm">
                    {{ record.prescription }}
                  </div>
                </div>
                
                <div class="col-md-12 mt-3" v-if="record.notes">
                  <label class="small fw-bold text-secondary text-uppercase ls-1">Doctor's Notes</label>
                  <p class="small text-muted fst-italic mt-1">{{ record.notes }}</p>
                </div>

              </div>
            </div>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/utils/api';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const history = ref([]);
const exportLoading = ref(false); 

onMounted(async () => {
  try {
    const userId = authStore.user.id;
    history.value = await api.get(`/patients/${userId}/history`);
  } catch (e) { console.error("Error fetching history", e); }
});

const exportData = async () => {
  if (history.value.length === 0) return;
  
  exportLoading.value = true;
  try {
    const res = await api.post('/export/history', {}); 
    
    alert(res.message || "Export started! Please check your email.");
  } catch (e) {
    alert("Failed to start export. Please try again later.");
    console.error(e);
  } finally {
    exportLoading.value = false;
  }
};
</script>

<style scoped>
.ls-1 {
  letter-spacing: 1px;
}
.accordion-button:not(.collapsed) {
  color: #0d6efd;
  background-color: #e7f1ff;
  box-shadow: none;
}
.accordion-button:focus {
  box-shadow: none;
  border-color: rgba(0,0,0,.125);
}
</style>