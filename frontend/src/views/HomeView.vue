<template>
  <CContainer class="mb-4">
    <div class="w-50 mx-auto mb-4 text-center">
      <h1 class="mt-3">Welcome to Song of the Week!</h1>
    </div>
  </CContainer>
  <div v-if="!isLoggedIn">
    <CContainer class="mb-4">
      <div class="d-flex justify-content-center">
        <CCard style="width: 24rem">
          <CCardBody class="text-center">
            <CCardTitle>It looks like you aren't signed in</CCardTitle>
            <CCardSubtitle class="mb-2 text-body-secondary">Please sign in or register to use Song of the Week
            </CCardSubtitle>
            <router-link :to="`/login`">
              <CButton color="primary" class="me-2">Login</CButton>
            </router-link>
            <router-link :to="`/register`">
              <CButton color="secondary" class="me-2">Register</CButton>
            </router-link>
          </CCardBody>
        </CCard>
      </div>
    </CContainer>

    <h2></h2>
    <p>
    </p>
    <h3></h3>
    <p>

    </p>

    <p>
    </p>
  </div>
  <div v-else class="text-center">
    <div v-if="user.sotw_list.length == 0">
      <h2>
        It looks like you are not a part of any Song of the Week competitions :( You can create one by clicking the
        button below, or you can join one by clicking on a share link that a friend sends you.
      </h2>
    </div>
    <div v-else>
      <h2>Choose a Song of the Week to enter or create a new one!</h2>
      <div class="row">
        <div class="col"></div>
        <div class="col-10 col-lg-3 p-4">
          <div class="list-group">
            <router-link v-for="sotw in user.sotw_list" class="list-group-item list-group-item-action"
              :to="`/sotw/` + sotw.id">{{ sotw.name }}</router-link>
          </div>
        </div>
        <div class="col"></div>
      </div>
    </div>
    <router-link to="/sotw/create">
      <button class="btn btn-outline-success" @click="create()">Create</button>
    </router-link>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import api from "@/shared/api";
import store from "@/store/index.js";
import {
  CButton,
  CContainer,
  CCard,
  CCardBody,
  CCardTitle,
  CCardSubtitle,
} from '@coreui/vue';

export default {
  name: "HomeView",
  components: {
    CButton,
    CContainer,
    CCard,
    CCardBody,
    CCardTitle,
    CCardSubtitle,
  },
  data() {
    return {
      sotwCreationModal: null,
    };
  },
  computed: {
    ...mapGetters({ sotw: "getActiveSotw", user: "getUser" }),
    isLoggedIn: () => {
      return store.getters.isAuthenticated;
    },
  },
  async mounted() {
    const vm = this;

    // check for redirection from spotify
    await vm.$router.isReady().then((_) => {
      if ("state" in vm.$route.query && vm.$route.query.state == vm.user.email + "-" + vm.user.name.replace(/\s+/g, '-')) {
        if ("code" in vm.$route.query) {
          const payload = {
            code: vm.$route.query.code,
            state: vm.$route.query.state,
          };
          // make api call to backend with the authorization code and update user on front end
          api.methods
            .apiUpdateUserSpotifyToken(payload)
            .then(async (res) => {
              await vm.getCurrentUser();
            })
            .then((_) => {
              vm.$router.push(sessionStorage.getItem("last_requested_path"));
            });
          // TODO maybe add toastr or modal or something to indicate spotify linked
        } else if ("error" in vm.$route.query) {
          console.log("ERROR", vm.$route.query.error);
          // TODO maybe add toastr or something to indicate spotify not linked
        }
      } else if (vm.$route.name == "verify") {
        // make api call to backend to verify the token and update user on front end
        api.methods
          .apiGetVerifyRegistration(vm.$route.params.verificationToken)
          .then(async (res) => {
            await vm.getCurrentUser();
          })
          .then((_) => {
            vm.$router.push("/link-spotify");
          })
          .catch((err) => {
            console.error("Invalid link:", err);
          });
      }

      vm.loginRegisterModal = new window.bootstrap.Modal("#loginModal");
      if (vm.isLoggedIn) {
        vm.sotwCreationModal = new window.bootstrap.Modal("#sotwCreationModal");
      }
    });
  },
  methods: {
    ...mapActions(["getSotw", "getCurrentUser"]),
    create() {
      const vm = this;
      if (!vm.sotwCreationModal._isShown) {
        vm.sotwCreationModal.show();
      }
    },
  },
};
</script>

<style scoped lang="scss">
.home {
  text-align: center;
}
</style>
