import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import AdminLayout from '@/pages/admin/AdminLayout.vue';
import AdminDashboard from '@/pages/admin/AdminDashboard.vue';
import AdminDoctors from '@/pages/admin/AdminDoctors.vue';
import AdminPatients from '@/pages/admin/AdminPatients.vue';
import AdminAppointments from '@/pages/admin/AdminAppointments.vue';
import ProfilePage from '@/pages/ProfilePage.vue';
import DoctorLayout from '@/pages/doctor/DoctorLayout.vue';
import DoctorDashboard from '@/pages/doctor/DoctorDashboard.vue';
import DoctorAppointments from '@/pages/doctor/DoctorAppointments.vue';
import DoctorPatients from '@/pages/doctor/DoctorPatients.vue';
import DoctorAvailability from '@/pages/doctor/DoctorAvailability.vue';
import LoginPage from '@/pages/LoginPage.vue'

import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'Home', component: HomePage },
    { path: '/login', name: 'Login', component: import('@/pages/LoginPage.vue') },
    { path: '/signup', name: 'Signup', component: import('@/pages/SignupPage.vue') },
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true, role: 'admin' },
      children: [
        { path: '', redirect: '/admin/dashboard' }, // Default redirect
        { path: 'dashboard', component: AdminDashboard },
        { path: 'doctors', component: AdminDoctors },
        { path: 'patients', component: AdminPatients },
        { path: 'appointments', component: AdminAppointments },
      ]
    },
    {
      path: '/doctor',
      component: DoctorLayout,
      meta: { requiresAuth: true, role: 'doctor' },
      children: [
        { path: '', redirect: '/doctor/dashboard' },
        { path: 'dashboard', component: DoctorDashboard },
        { path: 'appointments', component: DoctorAppointments },
        { path: 'patients', component: DoctorPatients },
        { path: 'availability', component: DoctorAvailability },
      ]
    },
    { 
      path: '/profile', 
      name: 'Profile', 
      component: ProfilePage, 
      meta: { requiresAuth: true } // Protect this route
    },
  ],
})
// Navigation Guard (Protects Admin Routes)
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  // 1. Check if route requires auth
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login');
  }

  // 2. Check for Admin Role
  if (to.meta.role === 'admin' && !authStore.isAdmin) {
    alert("Access Denied: Admins Only");
    return next('/');
  }

  next();
});
export default router
