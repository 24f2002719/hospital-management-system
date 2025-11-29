<template>
  <div class="d-flex flex-column min-vh-100 bg-light">

    <div class="container py-5">
      <div class="row justify-content-center">
        
        <div class="col-md-4 mb-4">
          <div class="card border-0 shadow-sm rounded-4 text-center p-4">
            <div class="card-body">
              <div class="bg-primary-subtle text-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 100px; height: 100px; font-size: 3rem;">
                👤
              </div>
              
              <h4 class="fw-bold mb-1">{{ authStore.userName }}</h4>
              <p class="text-muted mb-3">{{ form.email }}</p>
              
              <span v-if="authStore.isAdmin" class="badge bg-danger rounded-pill px-3">Administrator</span>
              <span v-else-if="authStore.isDoctor" class="badge bg-success rounded-pill px-3">Doctor</span>
              <span v-else class="badge bg-secondary rounded-pill px-3">Patient</span>

              <hr class="my-4">
              
              <div class="text-start">
                <p class="small text-muted fw-bold mb-1">MEMBER SINCE</p>
                <p>November 2025</p>
                <p class="small text-muted fw-bold mb-1">STATUS</p>
                <span class="text-success fw-bold">● Active</span>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-8">
          <div class="card border-0 shadow-sm rounded-4">
            <div class="card-header bg-white border-bottom-0 p-4 pb-0">
              <h4 class="fw-bold mb-0">Profile Settings</h4>
            </div>
            <div class="card-body p-4">
              
              <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
                {{ successMessage }}
                <button type="button" class="btn-close" @click="successMessage = ''"></button>
              </div>
              <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
                {{ errorMessage }}
                <button type="button" class="btn-close" @click="errorMessage = ''"></button>
              </div>

              <form @submit.prevent="updateProfile">
                <div class="row g-3">
                  
                  <div class="col-12">
                    <label class="form-label text-muted small fw-bold">EMAIL ADDRESS</label>
                    <input type="email" class="form-control bg-light" v-model="form.email" disabled>
                    <div class="form-text">Email cannot be changed. Contact admin for help.</div>
                  </div>

                  <div class="col-12">
                    <label class="form-label text-muted small fw-bold">FULL NAME</label>
                    <input type="text" class="form-control" v-model="form.name" required>
                  </div>

                  <div class="col-md-8">
                    <label class="form-label text-muted small fw-bold">ADDRESS</label>
                    <input type="text" class="form-control" v-model="form.address" placeholder="Street, City">
                  </div>

                  <div class="col-md-4">
                    <label class="form-label text-muted small fw-bold">PINCODE</label>
                    <input type="text" class="form-control" v-model="form.pincode" placeholder="000000">
                  </div>

                  <div class="col-12" v-if="authStore.isDoctor">
                    <label class="form-label text-muted small fw-bold">SPECIALIZATION</label>
                    <input type="text" class="form-control bg-light" :value="specialization" disabled>
                    <div class="form-text">Specialization can only be updated by Admin.</div>
                  </div>

                </div>

                <div class="d-flex justify-content-end mt-4">
                  <button type="submit" class="btn btn-primary rounded-pill px-4" :disabled="isLoading">
                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                    Save Changes
                  </button>
                </div>
              </form>

            </div>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import api from '@/utils/api';


const authStore = useAuthStore();

const isLoading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const specialization = ref(''); 

const form = ref({
  name: '',
  email: '',
  address: '',
  pincode: ''
});

const fetchProfile = async () => {
  try {
    const userId = authStore.user.id;
    
    const data = await api.get(`/users/${userId}`);
    
    form.value.name = data.name;
    form.value.email = data.email;
    form.value.address = data.address || '';
    form.value.pincode = data.pincode || '';
    
    if (data.specialization) {
      specialization.value = data.specialization;
    }

  } catch (error) {
    errorMessage.value = "Failed to load profile data.";
    console.error(error);
  }
};

const updateProfile = async () => {
  isLoading.value = true;
  successMessage.value = '';
  errorMessage.value = '';

  try {
    const userId = authStore.user.id;
    
    await api.put(`/users/${userId}`, {
      name: form.value.name,
      address: form.value.address,
      pincode: form.value.pincode
    });

    successMessage.value = "Profile updated successfully!";
    
    const updatedUser = { ...authStore.user, name: form.value.name };
    authStore.setUser(updatedUser);

  } catch (error) {
    errorMessage.value = error.message || "Failed to update profile.";
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchProfile();
});
</script>