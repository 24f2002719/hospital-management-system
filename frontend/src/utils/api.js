const baseURL = "http://127.0.0.1:5000/api";

const api = {
  async request(endpoint, options = {}) {
    const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
    const url = `${baseURL}${path}`;
    
    const token = localStorage.getItem("token");

    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    if (token) {
      headers["Authentication-Token"] = token;
    }

    const config = {
      ...options,
      headers,
    };

    try {
      const response = await fetch(url, config);

      if (response.status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        
        
        throw new Error("Session expired. Please login again.");
      }

      if (!response.ok) {
        let errorData = {};
        try {
          errorData = await response.json();
        } catch (e) {
        }
        
        const errorMessage = errorData.message || errorData.error || `HTTP error! status: ${response.status}`;
        
        const err = new Error(errorMessage);
        err.status = response.status;
        throw err;
      }

      if (response.status === 204) return null;
      
      const text = await response.text();
      if (!text) return null;
      
      try {
        return JSON.parse(text);
      } catch (e) {
        return text; 
      }

    } catch (error) {
      console.error(`API Request Failed: ${url}`, error);
      return Promise.reject(error);
    }
  },


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