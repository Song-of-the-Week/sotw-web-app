<template>
  <div class="modal fade" id="loginModal" tabindex="-1" role="dialog" aria-labelby="loginModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 v-if="registering" class="modal-title">Register</h5>
          <h5 v-else class="modal-title">Login</h5>
          <router-link :to="initialPath">
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
              @click="close()"
            ></button>
          </router-link>
        </div>
        <div class="modal-body">
          <!-- Register -->
          <form v-if="registering">
            <div class="mb-3">
              <label for="registerEmail" class="form-label" :class="{ invalid: !registerEmailValid }">
                Email Address
                <i
                  class="bi bi-question-circle"
                  data-bs-toggle="tooltip"
                  data-bs-title="Email will be used for login and password resetting."
                ></i>
              </label>
              <input
                v-model="registerForm.email"
                type="email"
                class="form-control"
                id="registerEmail"
                aria-describedby="emailHelp"
              />
              <p v-if="!registerEmailValid" class="invalid">Please provide a valid email address.</p>
            </div>
            <div class="mb-3">
              <label for="registerName" class="form-label" :class="{ invalid: !registerNameValid }">
                Name
                <i
                  class="bi bi-question-circle"
                  data-bs-toggle="tooltip"
                  data-bs-title="This name will be used publicly on the site to (potentially) announce you as a winner 
                  for others to see when guessing names. You will be able to change your name at any time."
                ></i>
              </label>
              <input
                v-model="registerForm.name"
                type="text"
                class="form-control"
                id="registerName"
                aria-describedby="nameHelp"
              />
              <p v-if="!registerNameValid" class="invalid">Name must be at least two characters long.</p>
            </div>
            <div class="mb-3">
              <label for="registerPassword" class="form-label" :class="{ invalid: !registerPasswordValid }">
                Password
                <i
                  class="bi bi-question-circle"
                  data-bs-toggle="tooltip"
                  data-bs-title="Password must be at least 8 characters long."
                ></i>
              </label>
              <PasswordInput
                id="registerPassword"
                @input-password="
                  (password) => {
                    registerForm.password = password;
                    validatePassword();
                  }
                "
              />
              <p v-if="!registerPasswordValid" class="invalid">Password must be at least 8 characters long.</p>
            </div>
            <div class="mb-3">
              <label
                for="registerPasswordConfirm"
                class="form-label"
                :class="{ invalid: !registerPasswordConfirmValid }"
                >Confirm Password</label
              >
              <PasswordInput
                id="registerPasswordConfirm"
                @input-password="
                  (password) => {
                    registerForm.passwordConfirm = password;
                    validatePasswordConfirm();
                  }
                "
              />
              <p v-if="!registerPasswordConfirmValid" class="invalid">Passwords must match.</p>
            </div>
            <div v-if="registerResponse400">
              <p class="invalid">{{ registerResponse400 }}</p>
            </div>
            <div v-if="registerResponse500">
              <p class="invalid">Sorry! Something went wrong... Please contact an administrator.</p>
            </div>
            <p>
              Already have an account? Click
              <router-link v-if="!loading" :to="`/login`">
                <a>here</a>
              </router-link>
              <a v-else href="#">here</a>
              to login.
            </p>
          </form>
          <!-- Login -->
          <form v-else id="login-form">
            <div class="mb-3">
              <label for="loginEmail" class="form-label" :class="{ invalid: !loginEmailValid }">Email Address</label>
              <input
                v-model="loginForm.email"
                type="email"
                class="form-control"
                id="loginEmail"
                aria-describedby="emailHelp"
              />
              <p v-if="!loginEmailValid" class="invalid">Email is invalid.</p>
            </div>
            <div class="mb-3">
              <label for="loginPassword" class="form-label" :class="{ invalid: !loginPasswordValid }">Password</label>
              <PasswordInput
                id="loginPassword"
                @input-password="
                  (password) => {
                    loginForm.password = password;
                  }
                "
              />
              <p v-if="!loginPasswordValid" class="invalid">Password is invalid.</p>
            </div>
            <div v-if="loginResponse400">
              <p class="invalid">{{ loginResponse400 }}</p>
            </div>
            <div v-if="loginResponse500">
              <p class="invalid">Sorry! Something went wrong... Please contact an administrator.</p>
            </div>
            <p>
              Forgot your password? Click
              <router-link v-if="!loading" :to="`/reset`">
                <a>here</a>
              </router-link>
              <a v-else href="#">here</a> to reset.
            </p>
            <p>
              Don't have an account? Click
              <router-link v-if="!loading" :to="`/register`">
                <a>here</a>
              </router-link>
              <a v-else href="#">here</a> to register.
            </p>
          </form>
        </div>
        <div class="modal-footer">
          <router-link :to="initialPath">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="close()">Close</button>
          </router-link>
          <div v-if="registering">
            <button v-if="loading" type="button" class="btn btn-primary btn-spinner-register">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </button>
            <button v-else type="button" class="btn btn-primary" @click="submitRegister()">Register</button>
          </div>
          <div v-else>
            <button v-if="loading" type="button" class="btn btn-primary btn-spinner-login">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </button>
            <button v-else type="button" class="btn btn-primary" @click="submitLogin()">Login</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import api from "@/shared/api";
import PasswordInput from "@/components/PasswordInput.vue";
import store from "@/store/index";
export default {
  name: "LoginRegisterModal",
  components: {
    PasswordInput,
  },
  props: {
    loginRegisterModal: {
      default: null,
    },
    registering: {
      type: Boolean,
      default: false,
    },
    initialPath: {
      type: String,
      default: "/",
    },
  },
  data() {
    return {
      loginForm: {
        email: "",
        password: "",
      },
      registerForm: {
        email: "",
        name: "",
        password: "",
        passwordConfirm: "",
      },
      validEmailRegex: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,
      loginEmailValid: true,
      loginPasswordValid: true,
      registerEmailValid: true,
      registerNameValid: true,
      registerPasswordValid: true,
      registerPasswordConfirmValid: true,
      loginResponse400: null,
      loginResponse500: false,
      registerResponse400: null,
      registerResponse500: false,
      loading: false,
    };
  },
  mounted() {
    const vm = this;

    // clean up modal form data on modal close
    document.getElementById("loginModal").addEventListener("hidden.bs.modal", function (_) {
      if (!vm.isLoggedIn) {
        sessionStorage.setItem("last_requested_path", "/");
      } else if (vm.sotw != null) {
        sessionStorage.setItem("last_requested_path", "/sotw/" + vm.sotw.id + "/survey");
      }
      vm.loginForm = {
        email: "",
        password: "",
      };
      vm.registerForm = {
        email: "",
        name: "",
        password: "",
        passwordConfirm: "",
      };
      vm.loginEmailValid = true;
      vm.loginPasswordValid = true;
      vm.registerEmailValid = true;
      vm.registerNameValid = true;
      vm.registerPasswordValid = true;
      vm.registerPasswordConfirmValid = true;
      vm.loginResponse400 = null;
      vm.loginResponse500 = false;
      vm.registerResponse400 = null;
      vm.registerResponse500 = false;
      // go to next route
      vm.$router.push(sessionStorage.getItem("last_requested_path"));
    });

    // submit form on enter key hit
    $(document).on("keypress", function (e) {
      if ($("#loginModal").hasClass("show") && (e.keycode == 13 || e.which == 13)) {
        e.preventDefault();
        if (vm.registering) {
          vm.submitRegister();
        } else {
          vm.submitLogin();
        }
      }
    });
  },
  computed: {
    ...mapGetters({ sotw: "getActiveSotw" }),
    isLoggedIn: () => {
      return store.getters.isAuthenticated;
    },
  },
  methods: {
    ...mapActions(["getCurrentUser"]),
    validatePassword() {
      const vm = this;
      // password validation
      if (vm.registerForm.password.length < 8) {
        vm.registerPasswordValid = false;
      } else {
        vm.registerPasswordValid = true;
      }
      vm.validatePasswordConfirm();
    },
    validatePasswordConfirm() {
      const vm = this;
      // password confirm validation
      if (vm.registerForm.password != vm.registerForm.passwordConfirm) {
        vm.registerPasswordConfirmValid = false;
      } else {
        vm.registerPasswordConfirmValid = true;
      }
    },
    async submitLogin() {
      const vm = this;

      vm.loading = true;
      vm.loginResponse400 = null;
      vm.loginResponse500 = false;

      // email validation
      if (!vm.loginForm.email.match(vm.validEmailRegex)) {
        vm.loginEmailValid = false;
      } else {
        vm.loginEmailValid = true;
      }
      // password validation
      if (vm.loginForm.password.length < 8) {
        vm.loginPasswordValid = false;
      } else {
        vm.loginPasswordValid = true;
      }

      if (vm.loginEmailValid && vm.loginPasswordValid) {
        // send login request
        await vm.login(vm.loginForm);
      } else {
        vm.loading = false;
      }
    },
    async submitRegister() {
      const vm = this;

      vm.loading = true;
      vm.registerResponse400 = null;
      vm.registerResponse500 = false;
      // email validation
      if (!vm.registerForm.email.match(vm.validEmailRegex)) {
        vm.registerEmailValid = false;
      } else {
        vm.registerEmailValid = true;
      }
      // name validation
      if (vm.registerForm.name.length < 2) {
        vm.registerNameValid = false;
      } else {
        vm.registerNameValid = true;
      }
      // password validation
      vm.validatePassword();

      if (
        vm.registerEmailValid &&
        vm.registerNameValid &&
        vm.registerPasswordValid &&
        vm.registerPasswordConfirmValid
      ) {
        // send register request
        await api.methods
          .apiPostRegister(vm.registerForm)
          .then(async (res) => {
            if (res.status == 201) {
              // get the spotify client id
              await api.methods.getSpotifyClientId().then((res) => {
                let params = new URLSearchParams({
                  client_id: res.data.client_id,
                  response_type: "code",
                  redirect_uri: config.SPOTIFY_CALLBACK_URI,
                  state: vm.registerForm.email + "-" + vm.registerForm.name,
                  scope: "playlist-modify-public",
                });
                document.location = `https://accounts.spotify.com/authorize?${params.toString()}`;
              });
            }
          })
          .catch((err) => {
            vm.loading = false;
            // error handling
            if (err.response.status == 400) {
              vm.registerResponse400 = err.response.data.detail;
            } else if (err.response.status == 500) {
              vm.registerResponse500 = true;
            } else {
              console.error("ERROR:", err);
            }
          });
      } else {
        vm.loading = false;
      }
    },
    async login(form) {
      const vm = this;
      let loginForm = new FormData();
      loginForm.append("username", form.email);
      loginForm.append("password", form.password);
      await api.methods
        .apiPostLogin(loginForm)
        .then(async (res) => {
          if (res.status == 200) {
            vm.loading = false;
            // set the user
            await vm.getCurrentUser();
            vm.loginRegisterModal.hide();
          }
        })
        .catch((err) => {
          vm.loading = false;
          // error handling
          console.error("ERROR:", err);
          if (err.response.status == 400) {
            vm.loginResponse400 = err.response.data.detail;
          } else if (err.response.status == 500) {
            vm.loginResponse500 = true;
          } else {
            console.error("ERROR:", err);
          }
        });
    },
    close() {
      const vm = this;
      vm.loginRegisterModal.hide();
    },
  },
  watch: {
    registering: function () {
      setTimeout(() => {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        [...tooltipTriggerList].map((tooltipTriggerEl) => new window.bootstrap.Tooltip(tooltipTriggerEl));
      }, 0);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
p {
  font-size: 0.84rem;
  margin: 0;
}
.invalid {
  color: #d91313;
}
.btn-spinner-register {
  width: 84.34px;
  height: 38px;
}
.btn-spinner-login {
  width: 66.3px;
  height: 38px;
}
.spinner-border {
  width: 1.4rem;
  height: 1.4rem;
}
</style>
