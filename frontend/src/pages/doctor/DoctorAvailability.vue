<template>
  <div class="card border-0 shadow-sm rounded-4">
    <div class="card-body p-4">
      
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-center mb-4 gap-3">
        <div>
          <h5 class="fw-bold mb-1">🕒 Manage Availability</h5>
          <p class="text-muted small mb-0">Set your working hours for the upcoming week.</p>
        </div>
        
        <div class="d-flex align-items-center gap-3">
          <div class="input-group input-group-sm">
            <span class="input-group-text bg-white">Slot Duration</span>
            <select v-model="slotDuration" class="form-select" style="max-width: 120px;">
              <option :value="30">30 Mins</option>
              <option :value="60">60 Mins</option>
            </select>
          </div>

          <button class="btn btn-success rounded-pill px-4 fw-bold" @click="saveAvailability" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ loading ? 'Saving...' : '💾 Save Schedule' }}
          </button>
        </div>
      </div>

      <div class="row g-3">
        <div class="col-md-6 col-lg-4" v-for="(day, index) in schedule" :key="index">
          <div 
            class="card h-100 border transition-all" 
            :class="day.active ? 'border-primary shadow-sm' : 'bg-light border-light text-muted'"
          >
            <div class="card-body">
              
              <div class="form-check form-switch mb-3 d-flex justify-content-between">
                <div>
                  <input class="form-check-input" type="checkbox" v-model="day.active" :id="'day-'+index">
                  <label class="form-check-label fw-bold ms-2" :for="'day-'+index">{{ day.displayDate }}</label>
                </div>
                <small class="text-primary fw-bold" v-if="day.active">{{ countSlots(day) }} Slots</small>
              </div>
              
              <div v-if="day.active">
                <div class="row g-2 align-items-center mb-3">
                  <div class="col-6">
                    <label class="small text-muted fw-bold mb-1">Start Time</label>
                    <input type="time" class="form-control" v-model="day.startTime">
                  </div>
                  <div class="col-6">
                    <label class="small text-muted fw-bold mb-1">End Time</label>
                    <input type="time" class="form-control" v-model="day.endTime">
                  </div>
                </div>

                <div class="bg-light p-2 rounded border border-light-subtle">
                  <p class="mb-1 small fw-bold text-secondary">Preview Slots:</p>
                  <div class="d-flex flex-wrap gap-1">
                    <span 
                      v-for="slot in generateSlotsPreview(day.startTime, day.endTime)" 
                      :key="slot" 
                      class="badge bg-white text-dark border fw-normal"
                    >
                      {{ slot }}
                    </span>
                    <span v-if="generateSlotsPreview(day.startTime, day.endTime).length === 0" class="text-danger small">
                      Invalid Range
                    </span>
                  </div>
                </div>
              </div>

              <div v-else class="text-center py-4 opacity-50">
                <span class="fs-4">💤</span>
                <p class="small mb-0">Day Off</p>
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

const loading = ref(false);
const schedule = ref([]);
const slotDuration = ref(60); 

const initSchedule = () => {
  const days = [];
  const today = new Date();
  
  for(let i=0; i<7; i++) {
    const d = new Date(today);
    d.setDate(today.getDate() + i);
    
    days.push({
      displayDate: d.toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' }),
      dbDate: d.toISOString().split('T')[0], 
      active: i < 5, 
      startTime: "09:00",
      endTime: "17:00"
    });
  }
  schedule.value = days;
};

const toMinutes = (timeStr) => {
  if (!timeStr) return 0;
  const [h, m] = timeStr.split(':').map(Number);
  return h * 60 + m;
};

const toTimeStr = (mins) => {
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
};

const generateSlotsPreview = (start, end) => {
  if (!start || !end) return [];
  
  const startMins = toMinutes(start);
  const endMins = toMinutes(end);
  const duration = slotDuration.value;
  
  const slots = [];
  let current = startMins;

  while (current + duration <= endMins) {
    slots.push(toTimeStr(current));
    current += duration;
  }
  
  return slots;
};

const countSlots = (day) => {
  return generateSlotsPreview(day.startTime, day.endTime).length;
};

const saveAvailability = async () => {
  loading.value = true;
  
  try {
    const payload = [];

    for (const day of schedule.value) {
      if (day.active) {
        const slotArray = generateSlotsPreview(day.startTime, day.endTime);
        const slotString = slotArray.join(',');

        if (slotString) {
          payload.push({
            date: day.dbDate, 
            slots: slotString 
          });
        }
      }
    }

    if (payload.length === 0) {
      alert("No active days selected. Please enable at least one day.");
      loading.value = false;
      return;
    }

    await api.post('/doctor/availability', payload);
    
    alert("Availability schedule updated successfully! Patients can now book these slots.");
    
  } catch (e) {
    console.error(e);
    alert("Failed to update availability: " + (e.message || "Unknown Error"));
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  initSchedule();
});
</script>

<style scoped>
.transition-all {
  transition: all 0.3s ease;
}
</style>