<template>
  <div>
    <table class="table table-responsive table-sm">
      <thead>
        <tr>
          <th scope="col" class="col-3">Name</th>
          <th scope="col" class="col-3 text">Results Release</th>
          <th scope="col" class="col-3">Invite Link</th>
          <th v-if="sotwList.some((sotw) => sotw.owner_id !== user.id)" scope="col" class="col-2">Leave</th>
          <th v-if="sotwList.some((sotw) => sotw.owner_id === user.id)" scope="col" class="col-2">Edit</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sotw in sotwList">
          <td>
            <div v-if="editing == sotw.id">
              <div class="row">
                <div class="col">
                  <input type="text" class="form-control competition-name-input" v-model="sotwName"
                    placeholder="Competition Name" aria-label="Competition Name" aria-describedby="basic-addon1" />
                  <p v-if="!sotwNameValid" class="invalid">Name must be at least two characters long.</p>
                </div>
              </div>
            </div>
            <div v-else>
              <button @click="setSotw(sotw.id)" class="btn btn-outline-primary">{{ sotw.name }}</button>
            </div>
          </td>
          <td v-if="editing == sotw.id" class="day-time-picker">
            <DayTimePicker :resultsDayTime="new Date(sotw.results_datetime)" :resultsTimezone="sotw.results_timezone"
              @input-day-time="(datetime) => {
                resultsDayTime = datetime.date;
                resultsTimezone = datetime.timezone;
              }" id="resultsDay" aria-describedby="resultsDayHelp" />
          </td>
          <td v-else>
            {{ sotw.results }}
          </td>
          <td v-if="sotw.share_link != null" class="text">
            <div class="row">
              <div class="col-6">
                <span>
                  {{ sotw.share_link }}
                </span>
              </div>
              <div class="col-3">
                <button @click="copy(sotw.share_link, sotw.id)" class="btn btn-outline-secondary float-start">
                  Copy
                </button>
              </div>
            </div>
          </td>
          <td v-else>
            <button v-if="loadingLink" class="btn btn-outline-secondary btn-spinner">
              <div class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </button>
            <button v-else @click="generateInviteLink(sotw.id)" class="btn btn-outline-secondary">
              Generate Invite Link
            </button>
          </td>
          <td>
            <button v-if="sotw.owner_id !== user.id" @click="showLeaveConfirm(sotw)" class="btn btn-outline-danger">Leave</button>
          </td>
          <td v-if="sotw.owner_id === user.id">
            <div v-if="editing == sotw.id">
              <div class="col-2 col-md-3">
                <button v-if="loadingEdit" type="button" class="btn btn-outline-info btn-spinner-sotw">
                  <div class="spinner-border spinner-border-sm" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </button>
                <div v-else>
                  <button type="button" class="btn btn-outline-info me-1" @click="submitEdit(sotw)">Save</button>
                  <button type="button" class="btn btn-outline-danger" @click="cancelEdit">Cancel</button>
                  <p v-if="updateResponse500" class="invalid">Something went wrong.</p>
                </div>
              </div>
            </div>
            <div v-else>
              <button @click="edit(sotw)" class="btn btn-outline-info">Edit</button>
            </div>
          </td>
          <td v-else>
          </td>
        </tr>
      </tbody>
    </table>
    <ConfirmationModal modalId="leaveConfirmModal" modalTitle="Confirm Leave"
      :modalBody="`Are you sure you want to leave &quot;${sotwToLeave?.name}&quot;?`" btnClass="btn-danger"
      buttonText="Leave" v-model:shouldShow="showLeaveModal" @click="confirmLeave" />
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import api from "@/shared/api";
import DayTimePicker from "./DayTimePicker.vue";
import ConfirmationModal from "./ConfirmationModal.vue";

export default {
  name: "SotwTable",
  components: {
    DayTimePicker,
    ConfirmationModal,
  },
  props: {
    sotwList: Array,
  },
  data() {
    return {
      loadingLink: false,
      editing: null,
      loadingEdit: false,
      sotwName: null,
      resultsDayTime: null,
      resultsTimezone: null,
      sotwNameValid: true,
      updateResponse500: false,
      showLeaveModal: false,
      sotwToLeave: null,
    };
  },
  computed: {
    ...mapGetters({ user: "getUser" }),
  },
  methods: {
    ...mapActions(["getSotw", "getCurrentUser", "updateSotw"]),
    setSotw(sotwId) {
      const vm = this;
      // set active sotw
      vm.getSotw(sotwId).then(() => {
        // set the active sotw in local storage for persistence
        // window.localStorage.setItem("activeSotwId", sotwId);
        // go to the home page
        vm.$router.push("/sotw/" + sotwId);
      });
    },
    copy(link, sotwId) {
      const vm = this;
      if (!vm.$cookies.isKey("invite-" + sotwId)) {
        alert("This link has expired, please generate a new one.");
        vm.$emit("build-sotw-list");
      } else {
        navigator.clipboard.writeText(link);
      }
    },
    async generateInviteLink(sotwId) {
      const vm = this;
      vm.loadingLink = true;
      await api.methods
        .apiGetSotwInviteLink(sotwId)
        .then((res) => {
          vm.$cookies.set("invite-" + sotwId, window.config.HOSTNAME + res.data.url, "30MIN");
          vm.$emit("build-sotw-list");
          vm.loadingLink = false;
        })
        .catch((err) => {
          alert("There was an error generating your share link:\n" + err);
          console.error(err);
        });
    },
    async leaveSotw(sotwId) {
      const vm = this;
      await api.methods
        .apiGetLeaveSotw(sotwId)
        .then((res) => {
          vm.getCurrentUser().then(() => {
            vm.$emit("build-sotw-list");
          });
        })
        .catch((err) => {
          console.error(err);
        });
    },
    showLeaveConfirm(sotw) {
      const vm = this;
      vm.sotwToLeave = sotw;
      vm.showLeaveModal = true;
    },
    async confirmLeave() {
      const vm = this;
      await vm.leaveSotw(this.sotwToLeave.id);
      vm.showLeaveModal = false;
      vm.sotwToLeave = null;
    },
    edit(sotw) {
      const vm = this;
      console.log(sotw)
      vm.editing = sotw.id;
      vm.sotwName = sotw.name;
      vm.resultsDayTime = new Date(sotw.results_datetime);
      vm.resultsTimezone = sotw.results_timezone;
    },
    cancelEdit() {
      const vm = this;
      vm.editing = null;
      vm.sotwName = null;
      vm.sotwNameValid = true;
    },
    submitEdit(sotw) {
      const vm = this;

      vm.sotwNameValid = vm.sotwName.length >= 2;

      if (vm.sotwNameValid) {
        vm.loadingEdit = true;
        let payload = {}
        if (vm.sotwName != sotw.name) {
          payload.name = vm.sotwName;
        }
        if (sotw.results_datetime != vm.resultsDayTime.getTime()) {
          payload.results_datetime = vm.resultsDayTime.getTime();
        }
        if (sotw.results_timezone != vm.resultsTimezone) {
          payload.results_timezone = vm.resultsTimezone;
        }

        if (payload.name == undefined && payload.results_datetime == undefined && payload.results_timezone == undefined) {
          vm.loadingEdit = vm.editing = false;
          return
        }
        vm.updateSotw({ id: sotw.id, payload: payload })
          .then((_) => {
            vm.getCurrentUser().then(() => {
              vm.$emit("build-sotw-list");
              vm.editing = false;
            });
          })
          .catch((err) => {
            if (err.cause == 500) {
              vm.updateResponse500 = true;
            } else {
              console.log("ERROR", err);
            }
            vm.sotwName = sotw.name;
            vm.resultsDayTime = new Date(sotw.results_datetime);
            vm.resultsTimezone = sotw.results_timezone;
          })
          .finally(() => {
            vm.loadingEdit = false;
          });
      }
    },
  },
};
</script>

<style scoped lang="scss">
.btn-spinner {
  width: 82.04px;
  height: 38px;
}

.btn-spinner-sotw {
  width: 54.75px;
  height: 38px;
}

.table td.text {
  max-width: 14rem;

  span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: inline-block;
    max-width: 100%;
  }
}

.table-responsive {
  overflow-x: auto;
}

.table th.text {
  span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: inline-block;
    max-width: 100%;
  }
}

.table th,
.table td {
  white-space: nowrap;
  /* Prevent wrapping */
}

.invalid {
  color: #d91313;
}

.day-time-picker {
  min-width: 24rem;
}

.competition-name-input {
  min-width: 12rem;
  /* Roughly 20 characters at default font size */
  width: 100%;
}
</style>
