// Patient History Page
<template>
  <div class="card border-0 shadow-sm rounded-4">
    <div class="card-body p-4">
      <h5 class="fw-bold mb-4">📂 Medical History</h5>
      
      <div v-if="history.length === 0" class="text-center py-5">
        <p class="text-muted">No past medical records found.</p>
      </div>

      <div v-else class="accordion" id="historyAccordion">
        <div class="accordion-item border-0 mb-3 shadow-sm rounded overflow-hidden" v-for="(record, index) in history" :key="record.id">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed fw-bold" type="button" data-bs-toggle="collapse" :data-bs-target="'#c'+index">
              {{ record.date }} - Dr. {{ record.doctor_name }}
            </button>
          </h2>
          <div :id="'c'+index" class="accordion-collapse collapse" data-bs-parent="#historyAccordion">
            <div class="accordion-body bg-light">
              <div class="row">
                <div class="col-md-12 mb-3">
                  <label class="small fw-bold text-muted">DIAGNOSIS</label>
                  <p class="fw-medium">{{ record.diagnosis }}</p>
                </div>
                <div class="col-md-12">
                  <label class="small fw-bold text-muted">PRESCRIPTION</label>
                  <div class="bg-white p-3 rounded border font-monospace">{{ record.prescription }}</div>
                </div>
                <div class="col-md-12 mt-3" v-if="record.notes">
                  <label class="small fw-bold text-muted">NOTES</label>
                  <p class="small text-secondary">{{ record.notes }}</p>
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

onMounted(async () => {
  try {
    // Fetch my own history
    const userId = authStore.user.id;
    history.value = await api.get(`/patients/${userId}/history`);
  } catch (e) { console.error(e); }
});
</script>