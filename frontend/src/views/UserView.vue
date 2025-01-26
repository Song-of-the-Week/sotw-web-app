<template>
  <div class="container-fluid">
    <div class="container">
      <h1 class="mt-3">Hello {{ user.name }}!</h1>
      <br />
      <div class="row">
        <div class="col">
          <h3>Account Info:</h3>
          <div v-if="editingName" class="row mt-3">
            <div class="col-3">Name:</div>
            <div class="col-6 col-md-5">
              <input type="text" class="form-control" v-model="userName" placeholder="Name" aria-label="Name"
                aria-describedby="basic-addon1" />
            </div>
            <div class="col-2 col-md-3">
              <button v-if="loadingName" type="button" class="btn btn-outline-warning btn-spinner">
                <div class="spinner-border spinner-border-sm" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </button>
              <button v-else type="button" class="btn btn-outline-info" @click="changeName">Save</button>
            </div>
          </div>
          <div v-else class="row mt-3">
            <div class="col-3">Name:</div>
            <div class="col-6 col-md-5 overflow-auto">
              {{ user.name }}
            </div>
            <div class="col-2 col-md-3">
              <button class="btn btn-outline-info" @click="editingName = true">Change</button>
            </div>
          </div>
          <div v-if="editingEmail" class="row mt-3">
            <div class="col-3">Email:</div>
            <div class="col-6 col-md-5">
              <input type="text" class="form-control" v-model="userEmail" placeholder="Email" aria-label="Email"
                aria-describedby="basic-addon1" />
            </div>
            <div class="col-2 col-md-3">
              <button v-if="loadingEmail" type="button" class="btn btn-outline-warning btn-spinner">
                <div class="spinner-border spinner-border-sm" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </button>
              <button v-else type="button" class="btn btn-outline-info" @click="changeEmail">Save</button>
            </div>
          </div>
          <div v-else class="row mt-3">
            <div class="col-3">Email:</div>
            <div class="col-6 col-md-5 overflow-auto">
              {{ user.email }}
            </div>
            <div class="col-2">
              <button class="btn btn-outline-info" @click="editingEmail = true">Change</button>
            </div>
          </div>
          <div class="row mt-3">
            <div class="col-3">Spotify Account:</div>
            <div v-if="user.spotify_linked" class="col-6 col-md-5">Linked ✅</div>
            <div v-if="user.spotify_linked" class="col-2">
              <button class="btn btn-outline-danger" @click="unlinkSpotify()">Unlink</button>
            </div>
            <div v-if="!user.spotify_linked" class="col-6 col-md-5">Not Linked ❌</div>
            <div v-if="!user.spotify_linked" class="col-2">
              <button class="btn btn-outline-success" @click="linkSpotify()">Link</button>
            </div>
          </div>
          <div v-if="editingPassword" class="row mt-3">
            <div class="col-12 pt-2 col-md-3 pt-md-0">
              <label for="currentPassword" class="form-label" :class="{ invalid: changePassword400.length > 0 }">Current
                Password</label>
              <PasswordInput id="currentPassword" @input-password="(password) => {
                  currentPassword = password;
                }
                " />
              <p v-if="changePassword400" class="invalid">{{ changePassword400 }}</p>
            </div>
            <div class="col-12 pt-2 col-md-3 pt-md-0">
              <label for="newPassword" class="form-label" :class="{ invalid: !newPasswordValid }">New Password</label>
              <PasswordInput id="newPassword" @input-password="(password) => {
                  newPassword = password;
                  validateNewPassword();
                }
                " />
              <p v-if="!newPasswordValid" class="invalid">Password must be at least 8 characters long.</p>
            </div>
            <div class="col-12 pt-2 col-md-3 pt-md-0">
              <label for="newPasswordConfirm" class="form-label" :class="{ invalid: !newPasswordConfirmValid }">Confirm
                New Password</label>
              <PasswordInput id="newPasswordConfirm" @input-password="(password) => {
                  newPasswordConfirm = password;
                  validateNewPasswordConfirm();
                }
                " />
              <p v-if="!newPasswordConfirmValid" class="invalid">Passwords must match.</p>
            </div>
            <div class="col-12 col-md-1 pt-md-0 pt-2rem pe-0">
              <button v-if="loadingPassword" type="button" class="btn btn-outline-warning btn-spinner-password">
                <div class="spinner-border spinner-border-sm" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </button>
              <button v-else type="button" class="btn btn-outline-info" @click="changePassword">Save</button>
            </div>
            <div class="col-12 col-md-2 pt-md-0 pt-2rem ps-0">
              <button type="button" class="btn btn-outline-warning" @click="editingPassword = false">Cancel</button>
            </div>
          </div>
          <div v-else class="row mt-3">
            <div class="col-6">
              <button class="btn btn-outline-warning" @click="editingPassword = true">Change Password</button>
            </div>
          </div>
          <div class="row mt-2">
            <div class="col">
              <p v-if="response500" class="invalid">Sorry! Something went wrong... Please contact an administrator.</p>
            </div>
          </div>
        </div>
      </div>
      <div class="row mt-3">
        <div class="col">
          <h3>Your Competitions:</h3>
        </div>
      </div>
      <div v-if="user.sotw_list.length == 0" class="row mt-3">
        <div class="col">
          <p>
            Looks like you're not a part of any Song of the Week competitions. Create a new competition or join an
            existing one to participate!
          </p>
        </div>
      </div>
      <div class="row mt-3">
        <div class="col">
          <SotwTable :sotwList="sotwList" @build-sotw-list="buildSotwList"></SotwTable>
        </div>
      </div>
      <div class="row mt-3 mb-3">
        <div class="col">
          <router-link to="/sotw/create">
            <button class="btn btn-outline-success" @click="create()">Create</button>
          </router-link>
        </div>
      </div>
    </div>
  </div>
  <AlertModal header="Email Change Verification" :message="`You're almost there! Please verify your new email via the link that was just sent to ` +
    userEmail +
    ` to complete your email change. The verification link will expire in 10 minutes.`
    "></AlertModal>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import api from "@/shared/api";
import config from "@/shared/config";
import AlertModal from "@/components/AlertModal.vue";
import PasswordInput from "@/components/PasswordInput.vue";
import SotwTable from "@/components/SotwTable.vue";

export default {
  name: "UserView",
  components: {
    AlertModal,
    PasswordInput,
    SotwTable,
  },
  data() {
    return {
      userName: "",
      userEmail: "",
      currentPassword: "",
      newPassword: "",
      newPasswordConfirm: "",
      editingName: false,
      editingEmail: false,
      editingPassword: false,
      loadingName: false,
      loadingEmail: false,
      loadingPassword: false,
      newPasswordValid: true,
      newPasswordConfirmValid: true,
      sotwList: [],
      changePassword400: "",
      response500: false,
      sotwCreationModal: null,
      alertModal: null,
    };
  },
  computed: {
    ...mapGetters({ user: "getUser" }),
  },
  mounted() {
    const vm = this;

    vm.getCurrentUser().then(() => {
      vm.userName = vm.user.name;
      vm.userEmail = vm.user.email;
    });

    vm.buildSotwList();

    vm.sotwCreationModal = new window.bootstrap.Modal("#sotwCreationModal");
    vm.alertModal = new window.bootstrap.Modal("#alertModal");

    if (vm.$route.name == "email") {
      // make api call to backend to verify the token and update user on front end
      api.methods
        .apiGetVerifyEmail(vm.$route.params.verificationToken)
        .then(async (res) => {
          await vm.getCurrentUser();
        })
        .catch((err) => {
          console.error("Invalid link:", err);
        });
    }
  },
  methods: {
    ...mapActions(["getCurrentUser", "updateUser"]),
    unlinkSpotify() {
      const vm = this;
      vm.updateUser({ spotify_linked: false }).catch((err) => {
        if (err.response.status == 500) {
          vm.response500 = true;
        } else {
          console.log("ERROR", err);
        }
      });
    },
    async linkSpotify() {
      const vm = this;
      sessionStorage.setItem("last_requested_path", "/user");
      await api.methods.getSpotifyClientId().then((res) => {
        let params = new URLSearchParams({
          client_id: res.data.client_id,
          response_type: "code",
          redirect_uri: config.SPOTIFY_CALLBACK_URI,
          state: vm.user.email + "-" + vm.user.name.replace(/\s+/g, '-'),
          scope: "playlist-modify-public",
        });
        document.location = `https://accounts.spotify.com/authorize?${params.toString()}`;
      });
    },
    changeName() {
      const vm = this;
      vm.loadingName = true;
      vm.updateUser({ name: vm.userName })
        .catch((err) => {
          if (err.response.status == 500) {
            vm.response500 = true;
          } else {
            console.log("ERROR", err);
          }
        })
        .finally(() => {
          vm.editingName = vm.loadingName = false;
          vm.userName = "";
        });
    },
    changeEmail() {
      const vm = this;
      if (vm.user.email == vm.userEmail) {
        vm.editingEmail = vm.loadingEmail = false;
        return;
      }
      vm.loadingEmail = true;
      vm.updateUser({ email: vm.userEmail })
        .then((_) => {
          vm.alertModal.show();
        })
        .catch((err) => {
          if (err.response.status == 500) {
            vm.response500 = true;
          } else {
            console.log("ERROR", err);
          }
        })
        .finally(() => {
          vm.editingEmail = vm.loadingEmail = false;
        });
    },
    changePassword() {
      const vm = this;
      vm.loadingPassword = true;
      vm.updateUser({ current_password: vm.currentPassword, new_password: vm.newPassword })
        .then((res) => {
          if (res && res.status == 200) {
            vm.currentPassword = vm.newPassword = vm.newPasswordConfirm = "";
            vm.editingPassword = false;
          }
        })
        .catch((err) => {
          if (400 <= err.response.status < 500) {
            vm.changePassword400 = err.response.data.detail;
          } else if (err.response.status >= 500) {
            vm.response500 = true;
          }
        })
        .finally(() => {
          vm.loadingPassword = false;
        });
    },
    validateNewPassword() {
      const vm = this;
      // password validation
      if (vm.newPassword.length < 8) {
        vm.newPasswordValid = false;
      } else {
        vm.newPasswordValid = true;
      }
      vm.validateNewPasswordConfirm();
    },
    validateNewPasswordConfirm() {
      const vm = this;
      // password confirm validation
      if (vm.newPassword != vm.newPasswordConfirm) {
        vm.newPasswordConfirmValid = false;
      } else {
        vm.newPasswordConfirmValid = true;
      }
    },
    buildSotwList() {
      const vm = this;
      vm.sotwList = [];

      // set sotwList for rendering
      const weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
      vm.user.sotw_list.forEach((sotw) => {
        const results = new Date(sotw.results_datetime);

        // check to see if there's a share link chached
        let shareLink = null;
        const shareCookieName = "invite-" + sotw.id;
        if (vm.$cookies.isKey(shareCookieName)) {
          shareLink = vm.$cookies.get(shareCookieName);
        }

        vm.sotwList.push({
          id: sotw.id,
          name: sotw.name,
          playlist_link: sotw.playlist_link,
          share_link: shareLink,
          results:
            weekday[results.getDay()] + " at " + results.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        });
      });
    },
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
@media only screen and (min-width: 768px) {
  .pt-2rem {
    padding-top: 2rem !important;
  }
}

.pt-2rem {
  padding-top: 1rem;
}

.btn-spinner {
  width: 82.04px;
  height: 38px;
}

.btn-spinner-password {
  width: 59.81px;
  height: 38px;
}

.invalid {
  color: #d91313;
}
</style>
