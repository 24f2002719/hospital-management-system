<template>
  <div class="d-flex flex-column min-vh-100 bg-white overflow-hidden">
    
    <header class="container pt-5 pb-3">
      <div class="row align-items-center flex-md-row-reverse py-4">
        <div class="col-12 col-md-6 mb-5 mb-md-0 position-relative">
          <div class="position-absolute top-50 start-50 translate-middle bg-primary opacity-25 rounded-circle blur-bg" style="width: 300px; height: 300px; z-index: -1;"></div>
          
          <img 
            src="https://img.freepik.com/free-vector/man-woman-accessing-medical-website_1262-19801.jpg?t=st=1764225353~exp=1764228953~hmac=9b5156d6f16f9afac8ffdb786224ec69101c1654667815faffea8355363b302d&w=2000" 
            class="d-block mx-lg-auto img-fluid rounded-5 shadow-lg border border-5 border-white" 
            alt="Hospital Management Hero" 
            loading="lazy"
            style="transform: scale(1.02);"
          >
        </div>
        
        <div class="col-12 col-md-6 pe-lg-5">
          <div class="d-inline-flex align-items-center rounded-pill bg-primary-subtle text-primary px-3 py-1 mb-4 fw-bold shadow-sm" style="font-size: 0.85rem;">
            <span class="badge bg-primary rounded-pill me-2">New</span> 
            Your trusted healthcare partner
          </div>

          <h1 class="display-3 fw-bolder text-dark mb-3 lh-sm ls-tight">
            Care. Manage. <br>
            <span class="text-primary text-gradient">Heal.</span>
          </h1>
          
          <p class="lead text-secondary mb-4" style="max-width: 500px;">
            A unified dashboard for managing patients, appointments, and staff. 
            Experience the next generation of healthcare administration.
          </p>

          <div class="d-flex gap-3 flex-column flex-sm-row">
            <router-link to="/signup" class="btn btn-primary btn-lg px-5 rounded-pill shadow-lg hover-lift">
              Get Started
            </router-link>
            <router-link to="/login" class="btn btn-outline-dark btn-lg px-5 rounded-pill hover-lift">
              Login
            </router-link>
          </div>

          <div class="mt-5 pt-3 border-top d-flex gap-4 text-secondary">
             <div class="d-flex align-items-center gap-2">
                <i class="fs-4">🛡️</i> <small>Secure Data</small>
             </div>
             <div class="d-flex align-items-center gap-2">
                <i class="fs-4">⚡</i> <small>Fast Support</small>
             </div>
          </div>
        </div>
      </div>
    </header>

    <section class="py-5 my-4">
        <div class="container">
            <div class="row row-cols-1 row-cols-md-3 g-4">
                <div class="col">
                    <div class="d-flex align-items-center gap-3 p-4 rounded-4 shadow-sm bg-white">
                        <div class="d-inline-flex align-items-center justify-content-center rounded-circle"
                                 style="width:64px;height:64px;background:linear-gradient(135deg,#0d6efd,#6610f2);color:white;font-size:1.25rem;box-shadow:0 8px 20px rgba(13,110,253,0.12);">
                            <!-- doctor / stethoscope icon -->
                            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                                <path d="M20 7v5a4 4 0 0 1-8 0V7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M12 7V5a2 2 0 1 0-4 0v2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                                <circle cx="20" cy="4" r="1.8" fill="currentColor"/>
                            </svg>
                        </div>
                        <div>
                            <div class="h3 fw-bold mb-0">500+</div>
                            <div class="text-muted small">Verified Doctors</div>
                        </div>
                    </div>
                </div>

                <div class="col">
                    <div class="d-flex align-items-center gap-3 p-4 rounded-4 shadow-sm bg-white">
                        <div class="d-inline-flex align-items-center justify-content-center rounded-circle"
                                 style="width:64px;height:64px;background:linear-gradient(135deg,#20c997,#0dcaf0);color:white;font-size:1.25rem;box-shadow:0 8px 20px rgba(32,201,151,0.12);">
                            <!-- patients / users icon -->
                            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                                <path d="M16 11a3 3 0 1 0-6 0" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M21 21v-1a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v1" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        <div>
                            <div class="h3 fw-bold mb-0">10k+</div>
                            <div class="text-muted small">Patients Served</div>
                        </div>
                    </div>
                </div>

                <div class="col">
                    <div class="d-flex align-items-center gap-3 p-4 rounded-4 shadow-sm bg-white">
                        <div class="d-inline-flex align-items-center justify-content-center rounded-circle"
                                 style="width:64px;height:64px;background:linear-gradient(135deg,#ff7b00,#ff4d6d);color:white;font-size:1.25rem;box-shadow:0 8px 20px rgba(255,123,0,0.12);">
                            <!-- 24/7 support / headset icon -->
                            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                                <path d="M3 13a9 9 0 1 1 18 0v3a2 2 0 0 1-2 2h-1" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M7 15v2a1 1 0 0 0 1 1h.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M17 15v2a1 1 0 0 1-1 1h-.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        <div>
                            <div class="h3 fw-bold mb-0">24/7</div>
                            <div class="text-muted small">Support & Response</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- optional micro-copy -->
            <div class="text-center mt-3">
                <small class="text-muted">Trusted by clinics and hospitals worldwide — secure, compliant, and easy to scale.</small>
            </div>
        </div>
    </section>

    <section class="bg-light py-5 position-relative">
      <div class="container py-5">
        <div class="text-center mb-5">
          <h6 class="text-primary fw-bold text-uppercase letter-spacing-2">Features</h6>
          <h2 class="fw-bold display-6">Why Choose Us?</h2>
          <p class="text-muted col-lg-6 mx-auto">
            Everything you need to run your clinic efficiently, packaged in a beautiful interface.
          </p>
        </div>

        <div class="row row-cols-1 row-cols-md-3 g-4">
          <div class="col" v-for="(feature, index) in features" :key="index">
            <div class="card h-100 border-0 shadow-sm rounded-5 p-4 hover-card transition-all bg-white">
              <div class="card-body text-center">
                <div class="feature-icon bg-primary bg-opacity-10 text-primary rounded-4 d-inline-flex align-items-center justify-content-center mb-4 shadow-sm" style="width: 70px; height: 70px; font-size: 2rem;">
                  {{ feature.icon }}
                </div>
                <h4 class="card-title fw-bold text-dark">{{ feature.title }}</h4>
                <p class="card-text text-secondary mt-3 leading-relaxed">
                  {{ feature.desc }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="container my-5 pb-5">
      <div class="position-relative p-5 text-center bg-dark text-white rounded-5 shadow-lg overflow-hidden">
        <div class="position-absolute top-0 start-0 w-100 h-100 bg-primary opacity-10" style="background: linear-gradient(45deg, #0d6efd, #6610f2);"></div>
        
        <div class="position-relative z-1 py-4">
          <h2 class="fw-bold display-6 mb-3">Ready to join our hospital?</h2>
          <p class="lead mb-4 col-lg-7 mx-auto text-white-50">
            Join thousands of healthcare professionals managing patient care efficiently with our trusted platform.
          </p>
          <router-link to="/signup" class="btn btn-light btn-lg px-5 rounded-pill fw-bold text-primary shadow hover-scale">
            Create Free Account
          </router-link>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref } from 'vue';

const features = ref([
  { 
    title: 'Smart Scheduling', 
    icon: '📅', 
    desc: 'Automated appointment booking system that prevents conflicts and sends reminders.' 
  },
  { 
    title: 'Digital Records', 
    icon: '📂', 
    desc: 'Securely store patient history with easy search and retrieval access for doctors.' 
  },
  { 
    title: 'Staff Portal', 
    icon: '👨‍⚕️', 
    desc: 'Dedicated dashboards for doctors to manage their availability and patient queues.' 
  }
]);
</script>

<style scoped>
/* Modern typography tweak */
.ls-tight {
  letter-spacing: -1px;
}

/* Blur effect behind hero image */
.blur-bg {
  filter: blur(60px);
}

/* Feature Card Hover Effect */
.hover-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 1rem 3rem rgba(0,0,0,.075) !important;
}

/* Button Lift Effect */
.hover-lift {
  transition: transform 0.2s;
}
.hover-lift:hover {
  transform: translateY(-3px);
}

/* CTA Button Scale Effect */
.hover-scale {
  transition: transform 0.2s;
}
.hover-scale:hover {
  transform: scale(1.05);
}
</style>