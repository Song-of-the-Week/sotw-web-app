<template>
  <div class="modal fade" id="sotwCreationModal" tabindex="-1" role="dialog" aria-labelby="sotwCreationModal"
    aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Create a Song of the Week</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="close()"></button>
        </div>
        <div class="modal-body">
          <form>
            <div class="mb-3">
              <label for="sotwName" class="form-label" :class="{ invalid: !sotwNameValid }">Name</label>
              <input v-model="sotwName" type="text" class="form-control" id="sotwName"
                aria-describedby="sotwNameHelp" />
              <p v-if="!sotwNameValid" class="invalid">Name must be at least two characters long.</p>
            </div>
            <div>
              <label for="resultsDayTime" class="form-label">
                Results Release Day and Time
                <i class="bi bi-question-circle" data-bs-toggle="tooltip"
                  data-bs-title="This will be the day of the week and time of day at which the results and the next survey are released each week."></i>
              </label>
              <DayTimePicker :resultsDayTime="resultsDayTime" :resultsTimezone="resultsTimezone" @input-day-time="(datetime) => {
                resultsDayTime = datetime.date;
                resultsTimezone = datetime.timezone;
              }" id="resultsDay" aria-describedby="resultsDayHelp" />
            </div>
            <div v-if="createResponse400">
              <p class="invalid">{{ createResponse400 }}</p>
            </div>
            <div v-if="createResponse500">
              <p class="invalid">Sorry! Something went wrong... Please contact an administrator.</p>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="close()">Close</button>
          <div>
            <button v-if="loading" type="button" class="btn btn-primary btn-spinner-create">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </button>
            <button v-else type="button" class="btn btn-primary" @click="submitCreate()">Create</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment-timezone";
import { mapActions, mapGetters } from "vuex";
import store from "@/store/index";
import DayTimePicker from "@/components/DayTimePicker.vue";
export default {
  name: "SotwCreationModal",
  components: {
    DayTimePicker,
  },
  props: {
    sotwCreationModal: {
      default: null,
    },
    initialPath: {
      type: String,
      default: "/",
    },
  },
  data() {
    return {
      sotwName: "",
      resultsDayTime: new Date(),
      resultsTimezone: "America/New_York",
      sotwNameValid: true,
      createResponse400: null,
      createResponse500: false,
      loading: false,
    };
  },
  mounted() {
    const vm = this;

    // initialize tooltips
    setTimeout(() => {
      const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
      [...tooltipTriggerList].map((tooltipTriggerEl) => new window.bootstrap.Tooltip(tooltipTriggerEl));
    }, 0);

    // clean up modal form data on modal close
    document.getElementById("sotwCreationModal").addEventListener("hidden.bs.modal", function (_) {
      vm.sotwName = "";
      vm.resultsDayTime = new Date();
      vm.resultsTimezone = moment.tz.guess();
      vm.sotwNameValid = true;
      vm.createResponse400 = null;
      vm.createResponse500 = false;
      vm.loading = false;

      // go back to initial path
      vm.$router.push(vm.initialPath);
      $(".modal-backdrop").remove();
    });

    // submit form on enter key hit
    $(document).on("keypress", function (e) {
      if ($("#sotwCreationModal").hasClass("show") && (e.keycode == 13 || e.which == 13)) {
        e.preventDefault();
        vm.submitCreate();
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
    ...mapActions(["createSotw", "getCurrentUser"]),
    submitCreate() {
      const vm = this;

      vm.sotwNameValid = vm.sotwName.length > 0;

      if (vm.sotwNameValid) {
        const payload = {
          name: vm.sotwName,
          results_datetime: vm.resultsDayTime.getTime(),
          results_timezone: vm.resultsTimezone,
        };
        vm.createSotw(payload)
          .then((_) => {
            // localStorage.setItem("activeSotwId", vm.sotw.id);
            // refresh the user to get the new sotw in the user
            vm.getCurrentUser();
            // close the modal
            vm.sotwCreationModal.hide();
          })
          .catch((err) => {
            if (err.cause >= 400 && err.cause < 500) {
              vm.createResponse400 = err.message;
            } else if (err.cause == 500) {
              vm.createResponse500 = true;
            } else {
              console.log("ERROR", err);
            }
          });
      }
    },
    close() {
      const vm = this;
      vm.sotwCreationModal.hide();
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

.btn-spinner-create {
  width: 73.7px;
  height: 38px;
}

.spinner-border {
  width: 1.4rem;
  height: 1.4rem;
}
</style>
