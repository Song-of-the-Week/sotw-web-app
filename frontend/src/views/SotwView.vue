<template>
  <div v-if="loading" class="home">
    <div class="spinner-border mt-5" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div v-else class="home">
    <h1 class="mt-3">Welcome to week {{ currentWeek.week_num }} of {{ sotw.name }}!</h1>
    <div v-if="!sotw">
      <h2>Blah Blah Blah!</h2>
    </div>
    <div v-else>
      <ul class="nav nav-tabs mb-3" id="myTab" role="tablist">
        <li class="nav-item" role="presentation">
          <router-link :to="`/sotw/` + sotw.id + `/survey`" class="nav-link"
            :class="activeClass('survey')">Survey</router-link>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" :class="activeClass('results') || activeClass('results_list')"
            data-bs-toggle="dropdown" href="#" role="button" aria-expanded="false">Results</a>
          <ul class="dropdown-menu">
            <li>
              <router-link :to="`/sotw/` + sotw.id + `/results/` + currentWeek.week_num"
                class="nav-link">Results</router-link>
            </li>
            <li>
              <router-link :to="`/sotw/` + sotw.id + `/results`" class="nav-link">Previous Results</router-link>
            </li>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle"
            :class="activeClass('playlist') || activeClass('soty') || activeClass('playlist_list')"
            data-bs-toggle="dropdown" href="#" role="button" aria-expanded="false">Playlists</a>
          <ul class="dropdown-menu">
            <li>
              <router-link :to="`/sotw/` + sotw.id + `/playlist/` + currentWeek.week_num" class="nav-link">Current
                Week's Playlist</router-link>
            </li>
            <li>
              <router-link :to="`/sotw/` + sotw.id + `/playlist/soty`" class="nav-link">Song of the Year
                Playlist</router-link>
            </li>
            <li>
              <router-link :to="`/sotw/` + sotw.id + `/playlist/master`" class="nav-link">All Songs
                Playlist</router-link>
            </li>
          </ul>
        </li>
        <li class="nav-item" role="tabpanel">
          <router-link :to="`/sotw/` + sotw.id + `/members`" class="nav-link"
            :class="activeClass('members')">Members</router-link>
        </li>
      </ul>
      <div class="tab-content" id="myTabContent">
        <div class="tab-pane fade" :class="activeClass('survey')" id="survey-tab-pane" role="tabpanel"
          aria-labelledby="survey-tab" tabindex="0">
          <Survey :survey-string="currentWeek.survey" :week="currentWeek" :week-error="currentWeekError" />
        </div>
        <div class="tab-pane fade" :class="activeClass('results')" id="current-results-tab-pane" role="tabpanel"
          aria-labelledby="results-tab" tabindex="0">
          <div v-if="renderResults">
            <Results :sotw-id="sotw.id" :week-num="resultsWeekNum" />
          </div>
        </div>
        <div class="tab-pane fade" :class="activeClass('results_list')" id="previous-results-tab-pane" role="tabpanel"
          aria-labelledby="results-tab" tabindex="0">
          <h1>Previous Results</h1>
          <div v-if="currentWeek.week_num < 2" class="row">
            <div class="col">
              <p>No previous results yet!</p>
            </div>
          </div>
          <div v-else class="row">
            <div class="col"></div>
            <div class="col-10 col-lg-3 p-4">
              <div class="list-group">
                <router-link v-for="n in currentWeek.week_num - 1" class="list-group-item list-group-item-action"
                  :to="`/sotw/` + sotw.id + `/results/` + (n + 1)">week {{ n }} results</router-link>
              </div>
            </div>
            <div class="col"></div>
          </div>
        </div>
        <div class="tab-pane fade spotify-playlist" :class="activeClass('playlist')" id="current-playlist-tab-pane"
          role="tabpanel" aria-labelledby="current-playlist-tab-pane" tabindex="0">
          <h1 v-if="currentWeek.week_num > 0">Current Playlist</h1>
          <SpotifyEmbed v-if="currentWeek.week_num > 0" :spotify-link="currentWeek.playlist_link" type="playlist" />
          <h1 v-if="currentWeek.week_num == 0">Come back next week for the first playlist!</h1>
        </div>
        <div class="tab-pane fade spotify-playlist" :class="activeClass('soty')" id="soty-playlist-tab-pane"
          role="tabpanel" aria-labelledby="soty-playlist-tab-pane" tabindex="0">
          <h1>Soty Playlist</h1>
          <SpotifyEmbed :spotify-link="sotw.soty_playlist_link" type="playlist" />
        </div>
        <div class="tab-pane fade spotify-playlist" :class="activeClass('playlist_list')" id="master-playlist-tab-pane"
          role="tabpanel" aria-labelledby="master-playlist-tab-pane" tabindex="0">
          <h1>Master Playlist</h1>
          <SpotifyEmbed :spotify-link="sotw.master_playlist_link" type="playlist" />
        </div>
        <div class="tab-pane fade" :class="activeClass('members')" id="members-tab-pane" role="tabpanel"
          aria-labelledby="members-tab" tabindex="0">
          <Members :sotw-id="sotw.id" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import Countdown from "@/components/Countdown.vue";
import Survey from "@/components/Survey.vue";
import Results from "@/components/Results.vue";
import SpotifyEmbed from "@/components/SpotifyEmbed.vue";
import Members from "@/components/Members.vue";

export default {
  name: "SotwView",
  components: {
    Countdown,
    Survey,
    Results,
    SpotifyEmbed,
    Members,
  },
  data() {
    return {
      renderResults: false,
      loading: false,
      resultsWeekNum: 0,
    };
  },
  computed: {
    ...mapGetters({
      sotw: "getActiveSotw",
      currentWeek: "getCurrentWeek",
      currentWeekError: "getCurrentWeekError",
      user: "getUser",
    }),
  },
  beforeMount() {
    const vm = this;

    vm.loading = true;
    vm.getSotw(vm.$route.params.sotwId)
      .then(() => {
        // localStorage.setItem("activeSotwId", vm.sotw.id);
        vm.loading = false;
      });
  },
  mounted() {
    const vm = this;

    vm.activeClass(vm.$route.name);
  },
  methods: {
    ...mapActions(["getSotw"]),
    activeClass(name) {
      const vm = this;
      if (name == vm.$route.name) {
        if (name == "results") {
          vm.resultsWeekNum = vm.$route.params.weekNum;
          vm.renderResults = true;
        } else {
          vm.renderResults = false;
        }
        return "show active";
      } else if (vm.$route.name == "sotw") {
        if (name == "members") {
          return "show active";
        }
        // calculate how far we are from the next release date
        if (Math.round((vm.currentWeek.next_results_release - new Date().getTime()) / (1000 * 3600 * 24)) < 5 || vm.currentWeek.week_num == 0) {
          if (name == "survey") {
            return "show active";
          }
        } else {
          if (name == "results") {
            vm.resultsWeekNum = vm.currentWeek.week_num;
            vm.renderResults = true;
            return "show active";
          }
        }
      }
    },
  },
};
</script>

<style scoped lang="scss">
.home {
  text-align: center;
}

.spotify-playlist {
  height: 70vh;
}
</style>
