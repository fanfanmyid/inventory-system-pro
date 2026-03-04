<template>
  <div class="landing-page">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <span class="navbar-brand" id="landing-brand">
          <i class="bi bi-box-seam me-2"></i>Inventory System Pro
        </span>
        <router-link to="/login" class="btn btn-outline-light btn-sm" id="btn-landing-login-top">
          Login
        </router-link>
      </div>
    </nav>

    <section class="hero py-5">
      <div class="container py-4">
        <div class="row align-items-center g-4">
          <div class="col-lg-7">
            <h1 class="display-5 fw-bold mb-3" id="landing-title">Manage Inventory and Sales with Confidence</h1>
            <p class="lead text-secondary mb-4" id="landing-subtitle">
              Full-stack demo project powered by FastAPI, Vue 3, PostgreSQL, Docker, Robot Framework, and now performance-tested with k6.
            </p>
            <div class="d-flex flex-wrap gap-2 mb-4">
              <span class="badge text-bg-primary p-2">FastAPI</span>
              <span class="badge text-bg-success p-2">Vue 3</span>
              <span class="badge text-bg-dark p-2">PostgreSQL</span>
              <span class="badge text-bg-warning p-2">Robot Framework</span>
              <span class="badge text-bg-info p-2">k6</span>
            </div>
            <div class="d-flex flex-wrap gap-3">
              <router-link to="/login" class="btn btn-primary btn-lg" id="btn-landing-login">
                <i class="bi bi-box-arrow-in-right me-2"></i>Login
              </router-link>
            </div>
          </div>
          <div class="col-lg-5">
            <div class="card shadow-sm border-0" id="landing-card-overview">
              <div class="card-body p-4">
                <h5 class="card-title mb-3">Project Preview</h5>
                <ul class="list-group list-group-flush small">
                  <li class="list-group-item px-0 d-flex justify-content-between">
                    <span>Inventory dashboard</span><i class="bi bi-check-circle-fill text-success"></i>
                  </li>
                  <li class="list-group-item px-0 d-flex justify-content-between">
                    <span>Sales & invoice history</span><i class="bi bi-check-circle-fill text-success"></i>
                  </li>
                  <li class="list-group-item px-0 d-flex justify-content-between">
                    <span>API & UI automation suites</span><i class="bi bi-check-circle-fill text-success"></i>
                  </li>
                  <li class="list-group-item px-0 d-flex justify-content-between">
                    <span>Dockerized deployment</span><i class="bi bi-check-circle-fill text-success"></i>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
</script>

<style scoped>
.hero {
  min-height: calc(100vh - 56px);
  display: flex;
  align-items: center;
}

.landing-page {
  background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
}
</style>
