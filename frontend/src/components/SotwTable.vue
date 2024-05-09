<template>
  <div class="table-responsive">
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Name</th>
          <th scope="col">Playlist Link</th>
          <th scope="col" class="text"><span>Survey Release</span></th>
          <th scope="col" class="text"><span>Results Release</span></th>
          <th scope="col">Invite Link</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sotw in sotwList">
          <td>
            <button @click="setSotw(sotw.id)" class="btn btn-outline-primary">{{ sotw.name }}</button>
          </td>
          <td>
            <a :href="sotw.playlist_link" target="_blank">{{ sotw.playlist_link }}</a>
          </td>
          <td>{{ sotw.results }}</td>
          <td>{{ sotw.survey }}</td>
          <td v-if="sotw.share_link != null" class="text">
            <div class="row">
              <div class="col">
                <span>
                  {{ sotw.share_link }}
                </span>
              </div>
              <div class="col">
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
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import api from "@/shared/api";

export default {
  name: "SotwTable",
  props: {
    sotwList: Array,
  },
  data() {
    return {
      loadingLink: false,
    };
  },
  computed: {
    ...mapGetters({ sotw: "getActiveSotw" }),
  },
  mounted() {},
  methods: {
    ...mapActions(["getSotw"]),
    setSotw(sotwId) {
      const vm = this;
      // set active sotw
      vm.getSotw(sotwId).then(() => {
        // set the active sotw in local storage for persistence
        window.localStorage.setItem("activeSotwId", sotwId);
        // go to the home page
        vm.$router.push("/sotw/" + sotwId);
      });
    },
    copy(link, sotwId) {
      const vm = this;
      if (!vm.$cookies.isKey("invite-" + sotwId)) {
        alert("This link has expired, please generate a new one.");
        vm.$emit("build-sotw-list", sotwId);
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
          vm.$cookies.set("invite-" + sotwId, window.config.HOSTNAME() + res.data.url, "30MIN");
          vm.$emit("build-sotw-list", sotwId);
          vm.loadingLink = false;
        })
        .catch((err) => {
          alert("There was an error generating your share link:\n" + err.response.data.detail);
          console.error(err);
        });
    },
  },
};
</script>

<style scoped lang="scss">
.btn-spinner {
  width: 82.04px;
  height: 38px;
}
.table td.text {
  span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: inline-block;
    max-width: 100%;
  }
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
</style>
