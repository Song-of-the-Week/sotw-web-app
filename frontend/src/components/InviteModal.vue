<template>
  <div class="modal fade" id="inviteModal" tabindex="-1" role="dialog" aria-labelby="inviteModal" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div v-if="response400" class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Looks like the link you used is no longer valid.</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>Please ask the person you got the invite link from to generate a new one for you.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
      <div v-else-if="response500" class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Oops! Something went wrong.</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>Please contact an administrator.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
      <div v-else-if="sotwRes.already_in" class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">You are already a part of {{ sotwRes.name }}!</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>You may proceed to {{ sotwRes.name }} by pressing "Continue" below.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" @click="cont()">Continue</button>
        </div>
      </div>
      <div v-else class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">You have been invited to join {{ sotwRes.name }}!</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>You may accept the invite to the Song of the Week competition by selecting "Join" below.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <div>
            <button v-if="loading" type="button" class="btn btn-primary btn-spinner-register">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </button>
            <button v-else type="button" class="btn btn-primary" @click="joinSotw()">Join</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import api from "@/shared/api";
export default {
  name: "InviteModal",
  props: {
    inviteModal: {
      default: null,
    },
  },
  data() {
    return {
      sotwRes: { already_in: false },
      loading: false,
      response400: false,
      response500: false,
    };
  },
  async mounted() {
    const vm = this;

    document.getElementById("inviteModal").addEventListener("shown.bs.modal", async function (_) {
      // get the sotw name
      await vm.getSotwName();
    });

    document.getElementById("inviteModal").addEventListener("hidden.bs.modal", function (_) {
      vm.sotwRes = { already_in: false };
      vm.loading = false;
      vm.response400 = vm.response500 = false;
    });
  },
  methods: {
    ...mapActions(["getSotw", "getCurrentUser"]),
    cont() {
      const vm = this;
      vm.inviteModal.hide();
      vm.$router.push("/sotw/" + vm.sotwRes.id);
    },
    async joinSotw() {
      const vm = this;

      // join the sotw via api
      vm.loading = true;
      await api.methods
        .apiGetSotwInviteJoin(vm.$route.params.shareToken)
        .then((res) => {
          // set the active sotw
          let sotwId = res.data.id;
          // localStorage.setItem("activeSotwId", sotwId);
          vm.getSotw(sotwId);
          // update the stored user in the front end
          vm.getCurrentUser();
          // close modal and redirect to the newly joined sotw
          vm.inviteModal.hide();
          vm.$router.push("/sotw/" + sotwId);
        })
        .catch((err) => {
          // error handling
          if (err.response.status == 403) {
            vm.response400 = true;
          } else if (err.response.status == 500) {
            vm.response500 = true;
          } else {
            console.error("ERROR:", err);
          }
        });
    },
    async getSotwName() {
      const vm = this;

      await api.methods
        .apiGetSotwInvitePending(vm.$route.params.shareToken)
        .then((res) => {
          vm.sotwRes = res.data;
        })
        .catch((err) => {
          // error handling
          if (err.response.status == 403) {
            vm.response400 = err.response.data.detail;
          } else if (err.response.status == 500) {
            vm.response500 = true;
          } else {
            console.error("ERROR:", err);
          }
        });
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
