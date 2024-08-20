<template>
  <div class="row">
    <div class="col">
      <h1 class="mt-3">Change Password</h1>
      <div class="row">
        <div class="col">
          <form>
            <div class="mb-3">
              <label for="password" class="form-label" :class="{ invalid: !passwordValid }">
                Password
                <i
                  class="bi bi-question-circle"
                  data-bs-toggle="tooltip"
                  data-bs-title="Password must be at least 8 characters long."
                ></i>
              </label>
              <PasswordInput
                id="password"
                @input-password="
                  (newPassword) => {
                    password = newPassword;
                    validatePassword();
                  }
                "
              />
              <p v-if="!passwordValid" class="invalid">Password must be at least 8 characters long.</p>
            </div>
            <div class="mb-3">
              <label for="passwordConfirm" class="form-label" :class="{ invalid: !passwordConfirmValid }"
                >Confirm Password</label
              >
              <PasswordInput
                id="passwordConfirm"
                @input-password="
                  (password) => {
                    passwordConfirm = password;
                    validatePasswordConfirm();
                  }
                "
              />
              <p v-if="!passwordConfirmValid" class="invalid">Passwords must match.</p>
            </div>
            <div v-if="response400">
              <p class="invalid">{{ response400 }}</p>
            </div>
            <div v-if="response500">
              <p class="invalid">Sorry! Something went wrong... Please contact an administrator.</p>
            </div>
          </form>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <button v-if="loading" type="button" class="btn btn-primary btn-spinner-login">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </button>
          <button v-else type="button" class="btn btn-primary" @click="submitPasswordChange()">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/shared/api";
import PasswordInput from "@/components/PasswordInput.vue";

export default {
  name: "PasswordResetView",
  components: { PasswordInput },
  data() {
    return {
      password: "",
      passwordConfirm: "",
      passwordValid: true,
      passwordConfirmValid: true,
      response400: null,
      response500: false,
    };
  },
  methods: {
    validatePassword() {
      const vm = this;
      // password validation
      vm.passwordValid = vm.password.length >= 8;
      vm.validatePasswordConfirm();
    },
    validatePasswordConfirm() {
      const vm = this;
      // password confirm validation
      vm.passwordConfirmValid = vm.password == vm.passwordConfirm;
    },
    submitPasswordChange() {
      const vm = this;

      vm.validatePassword();

      if (vm.passwordValid && vm.passwordConfirmValid) {
        api.methods
          .apiPostResetPasswordChange({ new_password: vm.password }, vm.$route.params.verificationToken)
          .then((res) => {
            if (res && res.status == 200) {
              vm.$router.replace("/login");
            }
          })
          .catch((err) => {
            if (400 <= err.response.status < 500) {
              vm.response400 = err.response.data.detail;
            } else if (err.response.status >= 500) {
              vm.response500 = true;
            } else {
              console.error("ERROR:", err);
            }
          });
      }
    },
  },
};
</script>

<style scoped lang="scss">
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
