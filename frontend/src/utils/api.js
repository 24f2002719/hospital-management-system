// Pointing to your Flask Backend
const baseURL = "http://127.0.0.1:5000/api";

const api = {
  async request(endpoint, options = {}) {
    // Ensure endpoint starts with a slash
    const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
    const url = `${baseURL}${path}`;
    
    // 1. Get Token (Updated to match your LoginPage key)
    const token = localStorage.getItem("token");

    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    // 2. Add Authentication Header (Matches Flask-Security config)
    if (token) {
      headers["Authentication-Token"] = token;
    }

    const config = {
      ...options,
      headers,
    };

    try {
      const response = await fetch(url, config);

      // 3. Handle Unauthorized (401) - Token expired or invalid
      if (response.status === 401) {
        // Clear data so Navbar updates correctly
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        
        // Optional: Force reload or redirect to login
        // window.location.href = '/login'; 
        
        throw new Error("Session expired. Please login again.");
      }

      // 4. Handle other HTTP Errors
      if (!response.ok) {
        let errorData = {};
        try {
          errorData = await response.json();
        } catch (e) {
          // If response isn't JSON, ignore
        }
        
        // Construct error message from Flask response
        // Flask usually sends { "message": "..." } or { "error": "..." }
        const errorMessage = errorData.message || errorData.error || `HTTP error! status: ${response.status}`;
        
        const err = new Error(errorMessage);
        err.status = response.status;
        throw err;
      }

      // 5. Handle Success (204 No Content vs JSON)
      if (response.status === 204) return null;
      
      const text = await response.text();
      if (!text) return null;
      
      try {
        return JSON.parse(text);
      } catch (e) {
        return text; // Fallback if server sends plain text
      }

    } catch (error) {
      console.error(`API Request Failed: ${url}`, error);
      return Promise.reject(error);
    }
  },

  // --- Convenience Methods ---

  get(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: "GET" });
  },

  post(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  put(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  patch(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "PATCH",
      body: JSON.stringify(data),
    });
  },

  delete(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: "DELETE" });
  },
};

export default api;