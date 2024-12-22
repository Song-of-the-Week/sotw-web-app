<template>
  <div class="container">
    <h2>Survey</h2>
    <div v-if="week.submitted">
      <div class="row">
        <div class="col col-10 col-sm-6 offset-1 offset-sm-3">
          <div class="card px-0 mb-4">
            <div class="card-header">Thank you for submitting!</div>
            <div v-if="weekError != null" class="card-body">
              <div class="row">
                <div class="col">
                  <p>Results for this week are not quite ready yet:</p>
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <p>{{ weekError }}</p>
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <button class="btn btn-outline-warning" @click="edit()">Edit Submission</button>
                </div>
              </div>
            </div>
            <div v-else class="card-body">
              <div class="row">
                <div class="col">
                  <p>Results for this week will be available in:</p>
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <Countdown :release-timestamp="week.next_results_release" />
                </div>
              </div>
              <div class="row">
                <div class="col">
                  <button class="btn btn-outline-warning" @click="edit()">Edit Submission</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <form v-else class="row form-horizontal justify-content-center" id="surveyForm" @submit.prevent="submit(false)">
      <!-- Pick your top 2 -->
      <div v-if="!week.week_num == 0" class="row" id="voteCard">
        <div class="col col-10 col-sm-6 offset-1 offset-sm-3">
          <div class="card px-0 mb-4" :class="{ invalid: !voteValid }">
            <div class="card-header">
              Pick your top 2
              <div v-if="!voteValid"><i class="bi bi-exclamation-circle"></i> Please pick 2 songs</div>
            </div>
            <div class="card-body">
              <ul class="list-group list-group-flush text-start" v-for="song in songs" :key="song.id">
                <li class="list-group-item">
                  <div class="row">
                    <div class="col col-1 align-self-center">
                      <input class="form-check-input me-3" type="checkbox" :value="song.id" v-model="pickedSongs"
                        :id="'vote-' + song.id"
                        :disabled="pickedSongs.length >= 2 && pickedSongs.indexOf(song.id) === -1" />
                    </div>
                    <div class="col">
                      <label class="form-check-label text-start" :for="'vote-' + song.id">{{ song.name }}</label>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <!-- Match user with song -->
      <div v-if="!week.week_num == 0" class="row" id="matchCard">
        <div class="col col-10 col-sm-6 offset-1 offset-sm-3">
          <div class="card px-0 mb-4" :class="{ 'match-invalid': !matchValid }">
            <div class="card-header" :class="{ invalid: !matchValid }">
              Matching
              <div v-if="!matchValid">
                <i class="bi bi-exclamation-circle"></i> Please match every person with a song
              </div>
            </div>
            <div class="card-body">
              <ul class="list-group-flush text-start" v-for="matchedSong in userSongMatches" :key="matchedSong.id">
                <li class="list-group-item">
                  <h5 class="card-title" :class="{ 'match-item-invalid': matchedSong.error }">
                    {{ matchedSong.song.name }}
                  </h5>
                </li>
                <li class="list-group-item dropdown">
                  <button class="btn btn-secondary dropdown-toggle" type="button" :id="'match-' + matchedSong.id"
                    data-bs-toggle="dropdown" aria-expanded="false">
                    <span v-if="matchedSong.user === undefined">Choose</span><span v-else>{{ matchedSong.user.name
                      }}</span>
                  </button>
                  <ul class="dropdown-menu" :aria-labelledby="'match-' + matchedSong.id">
                    <li v-for="user in users" :key="user.id">
                      <a class="dropdown-item" :class="{ 'text-muted': user.matched }"
                        @click="matchUserSong(matchedSong, user)">{{ user.name }}</a>
                    </li>
                  </ul>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <!-- Submit song link -->
      <div class="row" id="songCard">
        <div class="col col-10 col-sm-6 offset-1 offset-sm-3">
          <div class="card px-0 mb-4" :class="{ invalid: !songValid }">
            <div class="card-header">
              Submit next song (Spotify link)
              <div v-if="!songValid"><i class="bi bi-exclamation-circle"></i> Please submit a valid Spotify link</div>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col col-8 offset-2">
                  <input class="form-control" id="songInput" v-model="nextSong" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Submit -->
      <div v-if="!user.spotify_linked" class="row">
        <div class="col col-10 col-sm-6 offset-1 offset-sm-3 text-start">
          <p>You need to link your Spotify account to participate in Song of the Week.</p>
        </div>
      </div>
      <div class="row">
        <div class="col col-10 col-sm-6 offset-1 offset-sm-3 text-start">
          <button v-if="loading" type="button" class="btn btn-primary mb-3 btn-spinner-submit">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </button>
          <button v-else type="submit" class="btn btn-primary mb-3" :disabled="!user.spotify_linked">Submit</button>
        </div>
      </div>
    </form>
  </div>
  <!-- Modal -->
  <div class="modal fade" id="alertModal" tabindex="-1" role="dialog" aria-labelby="alertModal" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Alert!</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>
            The song you just submitted has already been submitted to this Song of the Week competition for a prior
            week. Would you like to submit it anyway?
          </p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Edit Submission</button>
          <div>
            <button v-if="loading" type="button" class="btn btn-primary btn-spinner-submit">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </button>
            <button v-else type="button" class="btn btn-primary" @click="submit(true)">Submit Anyway</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import api from "@/shared/api";
import Countdown from "@/components/Countdown.vue";
export default {
  name: "Survey",
  components: {
    Countdown,
  },
  props: {
    week: {
      default: null,
    },
    weekError: {
      default: null,
    },
  },
  data() {
    return {
      songs: [],
      users: [],
      pickedSongs: [],
      userSongMatches: [],
      nextSong: "",
      voteValid: true,
      matchValid: true,
      songValid: true,
      alertModal: null,
      submitted: false,
      loading: false,
    };
  },
  computed: {
    ...mapGetters({ user: "getUser" }),
  },
  mounted() {
    const vm = this;

    vm.alertModal = new window.bootstrap.Modal("#alertModal");
  },
  methods: {
    matchUserSong(song, user) {
      const vm = this;
      // remove the user from any other matches it has
      vm.userSongMatches.forEach((e) => {
        if (e.user === user) {
          e.user = undefined;
        }
      });
      // if the song has already been matched, unmatch the user before replacing the user
      if (song.user !== undefined) {
        song.user.matched = false;
      }
      song.user = user;
      song.user.matched = true;
    },
    edit() {
      const vm = this;
      vm.submitted = false;
    },
    async submit(repeatApproved = false) {
      const vm = this;

      vm.songValid = vm.nextSong.length != 0;
      if (!vm.songValid) {
        location.href = "#songCard";
      }

      if (vm.week.week_num == 0) {
        if (vm.songValid) {
          let payload = {
            next_song: vm.nextSong,
          };

          vm.submitSurvey(vm.$route.params.sotwId, vm.week.week_num, payload);
        }
      } else {
        // validate song matching
        let errCount = 0;
        vm.userSongMatches.forEach((e) => {
          e.error = e.user === undefined;
          if (e.error) {
            errCount++;
          }
        });

        vm.matchValid = errCount == 0;
        if (!vm.matchValid) {
          location.href = "#matchCard";
        }

        // validate voting
        vm.voteValid = vm.pickedSongs.length == 2;
        if (!vm.voteValid) {
          location.href = "#voteCard";
        }

        // send form data to back end
        if (vm.voteValid && vm.matchValid && vm.songValid) {
          // construct the payload
          let payloadMatches = [];
          vm.userSongMatches.forEach((match) => {
            payloadMatches.push({
              song_id: match.song.id,
              user_id: match.user.id,
            });
          });
          let payload = {
            picked_song_1: vm.pickedSongs[0],
            picked_song_2: vm.pickedSongs[1],
            user_song_matches: payloadMatches,
            next_song: vm.nextSong,
            repeat_approved: repeatApproved,
          };
          // send valid form data to back end to evaluate form and add to database
          vm.submitSurvey(vm.$route.params.sotwId, vm.week.week_num, payload);
        }
      }
    },
    async submitSurvey(sotwId, weekNum, payload) {
      const vm = this;
      vm.loading = true;
      console.log(payload.repeat_approved);
      await api.methods
        .apiPostSurveyResponse(sotwId, weekNum, payload)
        .then((res) => {
          if (res && res.status == 201) {
            if (!res.data.valid) {
              vm.songValid = false;
              location.href = "#songCard";
            } else if (res.data.repeat) {
              vm.alertModal.show();
            } else {
              vm.songValid = true;
              if (vm.alertModal._isShown) {
                vm.alertModal.hide();
              }
              location.href = "/sotw/" + sotwId;
            }
          }
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(() => {
          vm.loading = false;
        });
    },
  },
  watch: {
    week: {
      immediate: true,
      handler: function () {
        const vm = this;
        if (vm.week.survey.length != 0) {
          let surveyJson = JSON.parse(vm.week.survey);

          vm.userSongMatches = [];

          vm.songs = surveyJson.songs;
          vm.users = surveyJson.users;

          vm.songs.forEach((song) => {
            vm.userSongMatches.push({
              id: song.id,
              user: undefined,
              song: song,
              error: false,
            });
          });
        }
      },
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.invalid {
  color: #d91313;
  border-color: #d91313;
}

.match-invalid {
  border-color: #d91313;
}

.match-item-invalid {
  color: #d91313;
}

.btn-spinner-submit {
  width: 76.36px;
  height: 38px;
}

.spinner-border {
  width: 1.4rem;
  height: 1.4rem;
}
</style>
