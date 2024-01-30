<template>
  <div class="container">
    <h2>Survey</h2>
    <form class="row form-horizontal justify-content-center" id="surveyForm" @submit.prevent="submitSurvey">
      <!-- Pick your top 2 -->
      <div class="row" id="voteCard">
        <div class="col col-10 col-sm-6 offset-1 offset-sm-3">
          <div class="card px-0 mb-4" :class="{ invalid: !voteValid }">
            <div class="card-header">
              Pick your top 2
              <div v-if="!voteValid"><i class="bi bi-exclamation-circle"></i> Please pick 2 songs</div>
            </div>
            <div class="card-body">
              <ul class="list-group list-group-flush text-start" v-for="song in songs">
                <li class="list-group-item">
                  <div class="row">
                    <div class="col col-1 align-self-center">
                      <input
                        class="form-check-input me-3"
                        type="checkbox"
                        :value="song"
                        v-model="pickedSongs"
                        :id="'vote-' + song.id"
                        :disabled="pickedSongs.length >= 2 && pickedSongs.indexOf(song) === -1"
                      />
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
      <div class="row" id="matchCard">
        <div class="col col-10 col-sm-6 offset-1 offset-sm-3">
          <div class="card px-0 mb-4" :class="{ 'match-invalid': !matchValid }">
            <div class="card-header" :class="{ invalid: !matchValid }">
              Matching
              <div v-if="!matchValid">
                <i class="bi bi-exclamation-circle"></i> Please match every person with a song
              </div>
            </div>
            <div class="card-body">
              <ul class="list-group-flush text-start" v-for="matchedSong in matchedUserSongs">
                <li class="list-group-item">
                  <h5 class="card-title" :class="{ 'match-item-invalid': matchedSong.error }">
                    {{ matchedSong.song.name }}
                  </h5>
                </li>
                <li class="list-group-item dropdown">
                  <button
                    class="btn btn-secondary dropdown-toggle"
                    type="button"
                    :id="'match-' + matchedSong.id"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                  >
                    <span v-if="matchedSong.user === undefined">Choose</span
                    ><span v-else>{{ matchedSong.user.name }}</span>
                  </button>
                  <ul class="dropdown-menu" :aria-labelledby="'match-' + matchedSong.id">
                    <li v-for="user in users">
                      <a
                        class="dropdown-item"
                        :class="{ 'text-muted': user.matched }"
                        @click="matchUserSong(matchedSong, user)"
                        >{{ user.name }}</a
                      >
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
      <div class="row">
        <div class="col col-10 col-sm-6 offset-1 offset-sm-3 text-start">
          <button type="submit" class="btn btn-primary mb-3">Submit</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "Survey",
  props: {
    sotwId: String,
  },
  data() {
    return {
      songs: [],
      users: [],
      pickedSongs: [],
      matchedUserSongs: [],
      nextSong: "",
      voteValid: true,
      matchValid: true,
      songValid: true,
    };
  },
  computed: {},
  mounted() {
    const vm = this;
    // TODO make mock api calls using vuex
    vm.songs = [
      { id: 0, name: "Good Will Hunting - Black Country, New Road" },
      { id: 1, name: "Houdini - Dua Lipa" },
      { id: 2, name: "Here Comes the Sun - The Beatles" },
    ];
    vm.users = [
      { id: 0, name: "Jake", matched: false },
      { id: 1, name: "Joan", matched: false },
      { id: 2, name: "Daniel", matched: false },
    ];
    vm.songs.forEach((e) => {
      vm.matchedUserSongs.push({
        id: e.id,
        user: undefined,
        song: e,
        error: false,
      });
    });
  },
  methods: {
    matchUserSong(song, user) {
      const vm = this;
      // remove the user from any other matches it has
      vm.matchedUserSongs.forEach((e) => {
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
    async submitSurvey() {
      const vm = this;
      // validate spotify link
      if (vm.nextSong.length > 0) {
        // parse out the track id
        const trackId = vm.nextSong.split("/").pop().split("?")[0];
        // TODO send track id to API endpoint to validate the track on the back end
        vm.songValid = true;
      } else {
        vm.songValid = false;
        location.href = "#songCard";
      }

      // validate song matching
      let errCount = 0;
      vm.matchedUserSongs.forEach((e) => {
        if (e.user === undefined) {
          e.error = true;
          errCount++;
          console.log(errCount);
        } else {
          e.error = false;
        }
      });
      if (errCount !== 0) {
        vm.matchValid = false;
        location.href = "#matchCard";
      } else {
        console.log(errCount);
        vm.matchValid = true;
      }

      // validate voting
      if (vm.pickedSongs.length != 2) {
        vm.voteValid = false;
        location.href = "#voteCard";
      } else {
        vm.voteValid = true;
      }

      // send form data to back end
      if (vm.nameValid && vm.voteValid && vm.matchValid && vm.songValid) {
        let formData = {
          pickedSongs: vm.pickedSongs,
          matchedUserSongs: vm.matchedUserSongs,
          nextSong: vm.nextSong,
        };
        // TODO send valid form data to back end to evaluate form and add to database
        console.log(formData);
      }
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
</style>
