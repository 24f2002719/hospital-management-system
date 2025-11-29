import { defineStore } from "pinia";
import api from "@/utils/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null, 
    user: (() => {
      try {
        const raw = localStorage.getItem("user");
        return raw ? JSON.parse(raw) : null;
      } catch (e) {
        return null;
      }
    })(),
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    
    userName: (state) => state.user?.name || 'User',

    roles: (state) => state.user?.roles || [],
    isAdmin: (state) => state.user?.roles?.includes("admin"),
    isDoctor: (state) => state.user?.roles?.includes("doctor"),
    isPatient: (state) => state.user?.roles?.includes("patient"),
  },

  actions: {
    setToken(token) {
      this.token = token;
      if (token) {
        localStorage.setItem("token", token);
      } else {
        localStorage.removeItem("token");
      }
    },

    setUser(user) {
      this.user = user;
      if (user) {
        localStorage.setItem("user", JSON.stringify(user));
      } else {
        localStorage.removeItem("user");
      }
    },

    async login(email, password) {
      const data = await api.post("/auth/login", { email, password });
      
      if (data && data.user && data.user.token) {
        this.setToken(data.user.token);
        this.setUser(data.user);
        return true; 
      }
      throw new Error("Login failed: No token received");
    },

    async register(userData) {
      await api.post("/auth/register", userData);
    },

    logout() {
      this.setToken(null);
      this.setUser(null);
      window.location.href = '/login'; 
    },
  },
});