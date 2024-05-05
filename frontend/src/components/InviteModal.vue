<template>
  <div class="modal fade" id="inviteModal" tabindex="-1" role="dialog" aria-labelby="inviteModal" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">You have been invited to join {{ sotwName }}!</h5>
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
  props: {},
  data() {
    return {
      sotwName: "",
      loading: false,
    };
  },
  async mounted() {
    const vm = this;

    // get the sotw name
    await vm.getSotwName();
  },
  methods: {
    ...mapActions(["getSotw"]),
    async joinSotw() {
      const vm = this;

      // join the sotw via api
      vm.loading = true;
      await api.methods
        .apiGetSotwInviteJoin(vm.$route.params.shareToken)
        .then((res) => {
          // set the active sotw
          let sotwId = res.data.id;
          localStorage.setItem("activeSotwId", sotwId);
          vm.getSotw(sotwId);
          // redirect to the newly joined sotw
          window.location.pathname = "/sotw/" + sotwId;
          // clean up
          vm.loading = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async getSotwName() {
      const vm = this;

      await api.methods
        .apiGetSotwInvitePending(vm.$route.params.shareToken)
        .then((res) => {
          if ("name" in res.data) {
            vm.sotwName = res.data.name;
          } else {
            const activeSotwId = window.localStorage.setItem("activeSotwId", sotwId);
            if (activeSotwId) {
              vm.$router.push("/sotw/" + window.localStorage.getItem("activeSotwId"));
            } else {
              vm.$router.push("");
            }
          }
        })
        .catch((err) => {
          console.log(err);
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
