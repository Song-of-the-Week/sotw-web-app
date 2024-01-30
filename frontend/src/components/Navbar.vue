<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <router-link class="navbar-brand" :to="`/`">{{ sotwName }}</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        class="offcanvas offcanvas-end"
        tabindex="-1"
        id="navbarSupportedContent"
        aria-labelledby="navbarOffcanvasLgLabel"
      >
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasNavbarLabel">
            {{ sotwName }}
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <!-- <li class="nav-item">
              <a class="nav-link" href="#">About</a>
            </li> -->
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                id="navbarResultsDropdown"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                Results
              </a>
              <ul class="dropdown-menu" aria-labelledby="navbarResultsDropdown">
                <li>
                  <router-link class="dropdown-item" :to="`/results/...`">This Week's Results</router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" :to="`/results/...`">Previous Results</router-link>
                </li>
              </ul>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="`/data`">Data</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="`/playlists`">Playlists</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="`/rules`">Rules</router-link>
            </li>
            <!-- <li class="nav-item">
              <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
            </li> -->
          </ul>
          <div class="navbar-nav d-flex">
            <div class="nav-item">
              <router-link v-if="isLoggedIn" :to="`/`">
                <button class="btn btn-outline-success" @click="logout()">Logout</button>
              </router-link>
              <router-link v-else :to="`/login`">
                <button class="btn btn-outline-success">Login</button>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
  <LoginRegisterModal :registering="loginRegistering" />
</template>

<script>
import LoginRegisterModal from "@/components/LoginRegisterModal.vue";
import api from "@/shared/api";
import store from "@/store/index.js";
export default {
  name: "Navbar",
  components: {
    LoginRegisterModal,
  },
  props: {
    sotwName: {
      type: String,
      defualt: "Song of the Week",
    },
  },
  data: () => {
    return {
      loginRegisterModal: null,
      loginRegistering: false,
    };
  },
  computed: {
    isLoggedIn: () => {
      return store.getters.isAuthenticated;
    },
  },
  mounted() {
    const vm = this;

    vm.loginRegisterModal = new bootstrap.Modal("#loginModal");
  },
  methods: {
    logout() {
      console.log("whaaaaat");
    },
  },
  watch: {
    $route: {
      immediate: true,
      handler: function (newVal, oldVal) {
        const vm = this;

        if (vm.loginRegisterModal && newVal.meta) {
          if (newVal.meta.loginModal) {
            if (vm.loginRegisterModal._isShown) {
              vm.loginRegistering = false;
            } else {
              vm.loginRegistering = false;
              vm.loginRegisterModal.show();
            }
          } else if (newVal.meta.registerModal) {
            if (vm.loginRegisterModal._isShown) {
              vm.loginRegistering = true;
            } else {
              vm.loginRegistering = true;
              vm.loginRegisterModal.show();
            }
          }
        }
      },
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.router-link-exact-active {
  color: var(--bs-nav-link-color);
}
</style>
