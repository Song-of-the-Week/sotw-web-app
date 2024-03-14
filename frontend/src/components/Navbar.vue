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
            <div class="nav-item mb-2 mb-md-0 me-md-2" v-if="isLoggedIn">
              <router-link class="nav-link" :to="`/user`">My Profile</router-link>
            </div>
            <div class="nav-item">
              <router-link v-if="isLoggedIn" :to="`/`">
                <button class="btn btn-outline-success" @click="logoutUser()">Logout</button>
              </router-link>
              <router-link v-else :to="`/login`">
                <button class="btn btn-outline-success" @click="login()">Login</button>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
  <LoginRegisterModal :registering="loginRegistering" :login-register-modal="loginRegisterModal" />
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import LoginRegisterModal from "@/components/LoginRegisterModal.vue";
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
    ...mapGetters({ user: "getUser" }),
    isLoggedIn: () => {
      return store.getters.isAuthenticated;
    },
  },
  mounted() {
    const vm = this;

    vm.loginRegisterModal = new window.bootstrap.Modal("#loginModal");
  },
  methods: {
    ...mapActions(["logout"]),
    login() {
      const vm = this;
      if (!vm.loginRegisterModal._isShown) {
        vm.loginRegisterModal.show();
      }
    },
    logoutUser() {
      const vm = this;
      vm.logout().then(() => {
        this.$router.replace("/");
        vm.registering = false;
      });
    },
  },
  watch: {
    $route: {
      immediate: true,
      handler: function (newVal, _) {
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
