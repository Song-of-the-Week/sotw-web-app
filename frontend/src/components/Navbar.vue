<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <router-link class="navbar-brand ms-2" :to="`/`">Song of the Week</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="offcanvas offcanvas-end" tabindex="-1" id="navbarSupportedContent"
        aria-labelledby="navbarOffcanvasLgLabel">
        <div class="offcanvas-header">
          <router-link class="offcanvas-title navbar-brand" id="offcanvasNavbarLabel" :to="`/`"><span
              data-bs-dismiss="offcanvas">Song of the Week</span></router-link>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" :to="`/about`"><span data-bs-dismiss="offcanvas">About</span></router-link>
            </li>
            <li v-if="isLoggedIn" class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="navbarResultsDropdown" role="button"
                data-bs-toggle="dropdown" aria-expanded="false">
                SOTW
              </a>
              <ul class="dropdown-menu" aria-labelledby="navbarResultsDropdown">
                <span data-bs-dismiss="offcanvas">
                  <li v-for="sotw in user.sotw_list">
                    <router-link class="dropdown-item" :to="`/sotw/` + sotw.id">{{
                      sotw.name }}</router-link>
                  </li>
                </span>
              </ul>
            </li>
            <!-- <li class="nav-item">
              <router-link class="nav-link" :to="`/data`">Data</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="`/playlists`">Playlists</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="`/rules`">Rules</router-link>
            </li> -->
          </ul>
          <div class="navbar-nav d-flex">
            <div class="nav-item mb-2 mb-md-0 me-md-2" v-if="isLoggedIn">
              <router-link class="nav-link" :to="`/user`"><span data-bs-dismiss="offcanvas">My
                  Profile</span></router-link>
            </div>
            <div class="nav-item">
              <router-link v-if="isLoggedIn" :to="`/`">
                <button class="btn btn-outline-success" @click="logoutUser()">Logout</button>
              </router-link>
              <router-link v-else-if="!hideLoginButtonPaths.includes($route.path)" :to="`/login`">
                <button class="btn btn-outline-success" @click="login()">Login</button>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
  <!-- Modals -->
  <SpotifyModal></SpotifyModal>
  <LoginRegisterModal :registering="loginRegistering" :login-register-modal="loginRegisterModal"
    :initial-path="initialPath" />
  <InviteModal v-if="isLoggedIn" :invite-modal="inviteModal" />
  <SotwCreationModal v-if="isLoggedIn" :sotw-creation-modal="sotwCreationModal" :initial-path="initialPath" />
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import InviteModal from "@/components/InviteModal.vue";
import LoginRegisterModal from "@/components/LoginRegisterModal.vue";
import SotwCreationModal from "@/components/SotwCreationModal.vue";
import SpotifyModal from "@/components/SpotifyModal.vue";
import store from "@/store/index.js";
export default {
  name: "Navbar",
  components: {
    InviteModal,
    LoginRegisterModal,
    SotwCreationModal,
    SpotifyModal,
  },
  data: () => {
    return {
      inviteModal: null,
      loginRegisterModal: null,
      loginRegistering: false,
      sotwCreationModal: null,
      spotifyModal: null,
      initialPath: "/",
      hideLoginButtonPaths: ['/login', '/register', '/reset', '/'],
    };
  },
  computed: {
    ...mapGetters({ user: "getUser", sotw: "get" }),
    isLoggedIn: () => {
      return store.getters.isAuthenticated;
    },
  },
  mounted() {
    const vm = this;

    vm.loginRegisterModal = new window.bootstrap.Modal("#loginModal");
    if (vm.isLoggedIn) {
      vm.inviteModal = new window.bootstrap.Modal("#inviteModal");
      vm.sotwCreationModal = new window.bootstrap.Modal("#sotwCreationModal");
      vm.spotifyModal = new window.bootstrap.Modal("#spotifyModal");
      vm.getCurrentUser();
    }
  },
  methods: {
    ...mapActions(["logout", "getCurrentUser", "getSotw"]),
    login() {
      const vm = this;
      if (!vm.loginRegisterModal._isShown) {
        vm.loginRegisterModal.show();
      }
    },
    logoutUser() {
      const vm = this;
      vm.logout().then(() => {
        vm.$router.replace("/");
        vm.registering = false;
        sessionStorage.setItem("last_requested_path", "/");
      });
    },
    create() {
      const vm = this;
      if (!vm.sotwCreationModal._isShown) {
        vm.sotwCreationModal.show();
      }
    },
  },
  watch: {
    $route: {
      immediate: true,
      handler: function (newVal, oldVal) {
        // console.log("WHAT", newVal.path.split("/")[2]);
        const vm = this;

        if (
          oldVal &&
          oldVal.path.startsWith("/sotw/") &&
          newVal.path.startsWith("/sotw/") &&
          oldVal.path.split("/")[2] != newVal.path.split("/")[2]
        ) {
          vm.getSotw(newVal.path.split("/")[2]);
        }
        if (oldVal && oldVal.path != "/login" && oldVal.path != "/register" && oldVal.path != "/sotw/create") {
          vm.initialPath = oldVal.path;
        }

        if (newVal.meta) {
          if (vm.loginRegisterModal) {
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
          if (vm.inviteModal && newVal.meta.inviteModal && vm.user) {
            if (!vm.inviteModal._isShown) {
              vm.inviteModal.show();
            }
          }
          if (vm.sotwCreationModal && newVal.meta.createModal) {
            if (!vm.sotwCreationModal._isShown) {
              vm.sotwCreationModal.show();
            }
          }
          if (vm.spotifyModal && newVal.meta.spotifyModal) {
            if (!vm.spotifyModal.__isShown) {
              vm.spotifyModal.show();
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
