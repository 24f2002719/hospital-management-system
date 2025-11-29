<template>
  <div class="d-flex flex-column min-vh-100 bg-light">


    <div class="container py-5">
      <div class="row mb-4 align-items-center">
        <div class="col-md-6">
          <h2 class="fw-bold text-dark mb-1">Admin Portal</h2>
          <p class="text-muted mb-0">Manage hospital operations, staff, and patients.</p>
        </div>
        <div class="col-md-6 text-md-end mt-3 mt-md-0">
          <span class="badge bg-primary rounded-pill px-3 py-2">System Status: Online 🟢</span>
        </div>
      </div>

      <div class="card border-0 shadow-sm rounded-4 mb-4 overflow-hidden">
        <div class="card-body p-2">
          <nav class="nav nav-pills nav-fill gap-2 p-1">
            <router-link 
              to="/admin/dashboard" 
              class="nav-link fw-bold rounded-pill" 
              active-class="active shadow-sm"
            >
              📊 Dashboard
            </router-link>
            <router-link 
              to="/admin/doctors" 
              class="nav-link fw-bold rounded-pill" 
              active-class="active shadow-sm"
            >
              👨‍⚕️ Doctors
            </router-link>
            <router-link 
              to="/admin/patients" 
              class="nav-link fw-bold rounded-pill" 
              active-class="active shadow-sm"
            >
              🏥 Patients
            </router-link>
            <router-link 
              to="/admin/appointments" 
              class="nav-link fw-bold rounded-pill" 
              active-class="active shadow-sm"
            >
              📅 Appointments
            </router-link>
          </nav>
        </div>
      </div>

      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>

    </div>


  </div>
</template>



<style scoped>
.nav-pills .nav-link.active {
  background-color: #0d6efd;
  color: white;
}
.nav-pills .nav-link {
  color: #6c757d;
  transition: all 0.2s ease;
}
.nav-pills .nav-link:hover:not(.active) {
  background-color: #e9ecef;
  color: #0d6efd;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>