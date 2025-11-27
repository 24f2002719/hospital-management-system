import { defineStore } from "pinia";
import api from "@/utils/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    // matches the key used in your LoginPage.vue
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
    
    // Helper to get the user's name
    userName: (state) => state.user?.name || 'User',

    // Role Checks (Your backend sends roles as an array: ["admin"])
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
      // Uses your utils/api.js
      const data = await api.post("/auth/login", { email, password });
      
      // Your Flask backend returns: { user: { token: "...", id: 1, ... } }
      if (data && data.user && data.user.token) {
        this.setToken(data.user.token);
        this.setUser(data.user);
        return true; 
      }
      throw new Error("Login failed: No token received");
    },

    async register(userData) {
      // userData includes name, email, password, address, etc.
      await api.post("/auth/register", userData);
      // We don't log them in automatically after register, 
      // we usually send them to login page.
    },

    logout() {
      this.setToken(null);
      this.setUser(null);
      // Optional: Redirect to login or reload page
      window.location.href = '/login'; 
    },
  },
});