import { defineStore } from "pinia";
import api from "@/utils/api";

export const useHospitalStore = defineStore("hospital", {
  state: () => ({
    doctors: [],
    specializations: [],
    myAppointments: [], 
  }),

  getters: {
    appointmentCount: (state) => state.myAppointments.length,
    
    getDoctorById: (state) => (id) => state.doctors.find((d) => d.id === id),
  },

  actions: {
    async fetchSpecializations() {
      const data = await api.get("/specializations");
      this.specializations = Array.isArray(data) ? data : data.data || [];
    },

    async fetchDoctors() {
      const data = await api.get("/users?role=doctor"); 
      this.doctors = Array.isArray(data) ? data : data.data || [];
    },

    
    async bookAppointment(payload) {
      try {
        const result = await api.post("/appointments", payload);
        
        await this.fetchMyAppointments();
        return result;
      } catch (error) {
        throw error;
      }
    },

    async fetchMyAppointments() {
      const data = await api.get("/appointments");
      this.myAppointments = Array.isArray(data) ? data : data.data || [];
    },

    async cancelAppointment(appointmentId) {
      try {
        await api.delete(`/appointments/${appointmentId}`);
        this.myAppointments = this.myAppointments.filter(a => a.id !== appointmentId);
      } catch (error) {
        throw error;
      }
    }
  },
});