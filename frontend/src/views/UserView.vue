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
            <div class="col-5">
              <input
                type="text"
                class="form-control"
                v-model="userName"
                placeholder="Name"
                aria-label="Name"
                aria-describedby="basic-addon1"
              />
            </div>
            <div class="col-3">
              <button v-if="loadingName" type="button" class="btn btn-outline-warning btn-spinner">
                <div class="spinner-border" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </button>
              <button v-else type="button" class="btn btn-outline-info" @click="changeName">Save</button>
            </div>
          </div>
          <div v-else class="row mt-3">
            <div class="col-3">Name:</div>
            <div class="col-5">
              {{ user.name }}
            </div>
            <div class="col-3">
              <button class="btn btn-outline-info" @click="editingName = true">Change</button>
            </div>
          </div>
          <div v-if="editingEmail" class="row mt-3">
            <div class="col-3">Email:</div>
            <div class="col-5">
              <input
                type="text"
                class="form-control"
                v-model="userEmail"
                placeholder="Email"
                aria-label="Email"
                aria-describedby="basic-addon1"
              />
            </div>
            <div class="col-3">
              <button v-if="loadingEmail" type="button" class="btn btn-outline-warning btn-spinner">
                <div class="spinner-border" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </button>
              <button v-else type="button" class="btn btn-outline-info" @click="changeEmail">Save</button>
            </div>
          </div>
          <div v-else class="row mt-3">
            <div class="col-3">Email:</div>
            <div class="col-5">
              {{ user.email }}
            </div>
            <div class="col-3">
              <button class="btn btn-outline-info" @click="editingEmail = true">Change</button>
            </div>
          </div>
          <div class="row mt-3">
            <div class="col-6">
              <button class="btn btn-outline-warning" @click="changePassword">Change Password</button>
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
      editingName: false,
      editingEmail: false,
      loadingName: false,
      loadingEmail: false,
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
      console.log("uhm");
    },
  },
};
</script>

<style scoped lang="scss">
.btn-spinner {
  width: 82.04px;
  height: 38px;
}
</style>
