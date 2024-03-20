<template>
  <div
    class="modal fade"
    id="sotwCreationModal"
    tabindex="-1"
    role="dialog"
    aria-labelby="sotwCreationModal"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Create a Song of the Week</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form>
            <div class="mb-3">
              <label for="sotwName" class="form-label" :class="{ invalid: !sotwNameValid }"> Name </label>
              <input
                v-model="sotwName"
                type="text"
                class="form-control"
                id="sotwName"
                aria-describedby="sotwNameHelp"
              />
              <p v-if="!sotwNameValid" class="invalid">Name must be at least two characters long.</p>
            </div>
            <div class="mb-3">
              <label for="surveyDayTime" class="form-label">
                Survey Release Day and Time
                <i
                  class="bi bi-question-circle"
                  data-bs-toggle="tooltip"
                  data-bs-title="This will be the day of the week and time of day at which the survey is released each week."
                ></i>
              </label>
              <DayTimePicker
                @input-day-time="
                  (datetime) => {
                    surveyDayTime = datetime;
                  }
                "
                id="surveyDay"
                aria-describedby="surveyDayHelp"
              />
            </div>
            <div>
              <label for="resultsDayTime" class="form-label">
                Results Release Day and Time
                <i
                  class="bi bi-question-circle"
                  data-bs-toggle="tooltip"
                  data-bs-title="This will be the day of the week and time of day at which the results is released each week."
                ></i>
              </label>
              <DayTimePicker
                @input-day-time="
                  (datetime) => {
                    resultsDayTime = datetime;
                  }
                "
                id="resultsDay"
                aria-describedby="resultsDayHelp"
              />
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
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <div>
            <button v-if="loading" type="button" class="btn btn-primary btn-spinner-register">
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
  },
  data() {
    return {
      sotwName: "",
      surveyDayTime: new Date(),
      resultsDayTime: new Date(),
      sotwNameValid: true,
      createResponse400: null,
      createResponse500: false,
      loading: false,
    };
  },
  mounted() {
    const vm = this;

    // clean up modal form data on modal close
    document.getElementById("sotwCreationModal").addEventListener("hidden.bs.modal", function (_) {
      vm.sotwName = "";
      vm.surveyDayTime = new Date();
      vm.resultsDayTime = new Date();
      vm.sotwNameValid = true;
      vm.createResponse400 = null;
      vm.createResponse500 = false;
      vm.loading = false;
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
        let payload = {
          name: vm.sotwName,
          survey_datetime: vm.surveyDayTime,
          results_datetime: vm.resultsDayTime,
        };
        // TODO: add api call here and update sotw.js in store
        vm.createSotw(payload)
          .then((res) => {
            localStorage.setItem("activeSotwId", vm.sotw.id);
          })
          .catch((err) => {
            if (err.response.status == 500) {
              vm.response500 = true;
            } else {
              console.log("ERROR", err);
            }
          })
          .finally(() => {
            // refresh the user to get the new sotw in the user
            vm.getCurrentUser();
          });
      }
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
