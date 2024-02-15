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
              <input
                type="text"
                class="form-control"
                v-model="userName"
                placeholder="Name"
                aria-label="Name"
                aria-describedby="basic-addon1"
              />
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
            <div class="col-6 col-md-5">
              {{ user.name }}
            </div>
            <div class="col-2 col-md-3">
              <button class="btn btn-outline-info" @click="editingName = true">Change</button>
            </div>
          </div>
          <div v-if="editingEmail" class="row mt-3">
            <div class="col-3">Email:</div>
            <div class="col-6 col-md-5">
              <input
                type="text"
                class="form-control"
                v-model="userEmail"
                placeholder="Email"
                aria-label="Email"
                aria-describedby="basic-addon1"
              />
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
            <div class="col-6 col-md-5">
              {{ user.email }}
            </div>
            <div class="col-2">
              <button class="btn btn-outline-info" @click="editingEmail = true">Change</button>
            </div>
          </div>
          <div v-if="editingPassword" class="row mt-3">
            <div class="col-12 pt-2 col-md-3 pt-md-0">
              <label for="currentPassword" class="form-label" :class="{ invalid: !currentPasswordValid }"
                >Current Password</label
              >
              <PasswordInput
                id="currentPassword"
                @input-password="
                  (password) => {
                    currentPassword = password;
                  }
                "
              />
              <p v-if="!currentPasswordValid" class="invalid">Incorrect password.</p>
            </div>
            <div class="col-12 pt-2 col-md-3 pt-md-0">
              <label for="newPassword" class="form-label" :class="{ invalid: !newPasswordValid }">New Password</label>
              <PasswordInput
                id="newPassword"
                @input-password="
                  (password) => {
                    newPassword = password;
                    validateNewPassword();
                  }
                "
              />
              <p v-if="!newPasswordValid" class="invalid">Password must be at least 8 characters long.</p>
            </div>
            <div class="col-12 pt-2 col-md-3 pt-md-0">
              <label for="newPasswordConfirm" class="form-label" :class="{ invalid: !newPasswordConfirmValid }"
                >Confirm New Password</label
              >
              <PasswordInput
                id="newPasswordConfirm"
                @input-password="
                  (password) => {
                    newPasswordConfirm = password;
                    validateNewPasswordConfirm();
                  }
                "
              />
              <p v-if="!newPasswordConfirmValid" class="invalid">Passwords must match.</p>
            </div>
            <div class="col-12 col-md-3 pt-md-0 pt-2rem">
              <button v-if="loadingPassword" type="button" class="btn btn-outline-warning btn-spinner-password">
                <div class="spinner-border spinner-border-sm" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </button>
              <button v-else type="button" class="btn btn-outline-info" @click="changePassword">Save</button>
            </div>
          </div>
          <div v-else class="row mt-3">
            <div class="col-6">
              <button class="btn btn-outline-warning" @click="editingPassword = true">Change Password</button>
            </div>
          </div>
        </div>
      </div>
      <div class="row mt-3">
        <div class="col">
          <h3>Sotws:</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import PasswordInput from "@/components/PasswordInput.vue";

export default {
  name: "UserView",
  components: {
    PasswordInput,
  },
  data() {
    return {
      userName: null,
      userEmail: null,
      currentPassword: "",
      newPassword: "",
      newPasswordConfirm: "",
      editingName: false,
      editingEmail: false,
      editingPassword: false,
      loadingName: false,
      loadingEmail: false,
      loadingPassword: false,
      currentPasswordValid: true,
      newPasswordValid: true,
      newPasswordConfirmValid: true,
    };
  },
  computed: {
    ...mapGetters({ user: "getUser" }),
  },
  mounted() {
    const vm = this;

    vm.userName = vm.user.name;
    vm.userEmail = vm.user.email;
  },
  methods: {
    ...mapActions(["updateUser"]),
    changeName() {
      const vm = this;
      vm.loadingName = true;
      vm.updateUser({ name: vm.userName })
        .then((res) => {
          vm.editingName = vm.loadingName = false;
        })
        .catch((err) => {
          vm.editingName = vm.loadingName = false;
          console.error(err);
        });
    },
    changeEmail() {
      const vm = this;
      vm.loadingEmail = true;
      vm.updateUser({ email: vm.userEmail })
        .then((res) => {
          vm.editingEmail = vm.loadingEmail = false;
        })
        .catch((err) => {
          vm.editingEmail = vm.loadingEmail = false;
          console.error(err);
        });
    },
    changePassword() {
      const vm = this;
      vm.loadingPassword = true;
      setTimeout(() => {
        vm.editingPassword = vm.loadingPassword = false;
      }, 1000);
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
