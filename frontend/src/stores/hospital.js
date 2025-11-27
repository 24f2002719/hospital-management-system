import { defineStore } from "pinia";
import api from "@/utils/api";

export const useHospitalStore = defineStore("hospital", {
  state: () => ({
    doctors: [],
    specializations: [],
    myAppointments: [], // The user's "Cart" of booked slots
  }),

  getters: {
    // Equivalent to "cart.count"
    appointmentCount: (state) => state.myAppointments.length,
    
    // Helper to find a doctor by ID
    getDoctorById: (state) => (id) => state.doctors.find((d) => d.id === id),
  },

  actions: {
    // --- 1. Fetch Data (Like loading products) ---
    async fetchSpecializations() {
      const data = await api.get("/specializations");
      // Flask returns a list directly or { data: [] }
      this.specializations = Array.isArray(data) ? data : data.data || [];
    },

    async fetchDoctors() {
      // Assuming you create a public endpoint for this
      const data = await api.get("/users?role=doctor"); 
      this.doctors = Array.isArray(data) ? data : data.data || [];
    },

    // --- 2. Manage Appointments (Like Add/Remove Item) ---
    
    // "Add to Cart" -> Book Appointment
    async bookAppointment(payload) {
      // payload = { doctor_id, appointment_date, appointment_time }
      try {
        const result = await api.post("/appointments", payload);
        
        // Refresh the list after booking
        await this.fetchMyAppointments();
        return result;
      } catch (error) {
        throw error;
      }
    },

    // "Get Cart Items" -> Get My Appointments
    async fetchMyAppointments() {
      // Assuming /appointments returns the logged-in user's history
      const data = await api.get("/appointments");
      this.myAppointments = Array.isArray(data) ? data : data.data || [];
    },

    // "Remove Item" -> Cancel Appointment
    async cancelAppointment(appointmentId) {
      try {
        await api.delete(`/appointments/${appointmentId}`);
        // Remove from local state immediately for UI responsiveness
        this.myAppointments = this.myAppointments.filter(a => a.id !== appointmentId);
      } catch (error) {
        throw error;
      }
    }
  },
});