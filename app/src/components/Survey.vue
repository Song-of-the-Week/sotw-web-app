<template>
  <div class="container">
    <h2>Survey</h2>
    <form class="row form-horizontal justify-content-center" @submit.prevent="submitSurvey">
      <!-- Name -->
      <div class="row">
        <div class="col col-10 col-sm-6 offset-1 offset-sm-3">
          <div class="card px-0 mb-4">
            <div class="card-header">
              Who ye be?
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col col-8 offset-2">
                  <input class="form-control" id="nameInput" v-model="userName" required>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Pick your top 2 -->
      <div class="row">
        <div class="col col-10 col-sm-6 offset-1 offset-sm-3">
          <div class="card px-0 mb-4">
            <div class="card-header">
              Pick your top 2
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
                        :id="song.id"
                        :disabled="pickedSongs.length >= 2 && pickedSongs.indexOf(song) === -1"
                      >
                    </div>
                    <div class="col">
                      <label class="form-check-label text-start" :for="song.id">{{ song.name }}</label>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <!-- Match user with song -->
      <div class="row">
        <div class="col col-10 col-sm-6 offset-1 offset-sm-3">
          <div class="card px-0 mb-4">
            <div class="card-header">
              Matching
            </div>
            <div class="card-body">
              <ul class="list-group-flush text-start" v-for="matchedSong in matchedUserSongs">
                <li class="list-group-item">
                  <h5 class="card-title">{{ matchedSong.song.name }}</h5>
                </li>
                <li class="list-group-item dropdown">
                  <button 
                    class="btn btn-secondary dropdown-toggle"
                    type="button"
                    :id="matchedSong.id"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                  ><span v-if="matchedSong.user === undefined">Choose</span><span v-else>{{ matchedSong.user.name }}</span></button>
                  <ul class="dropdown-menu" :aria-labelledby="matchedSong.id">
                    <li v-for="user in users">
                      <a class="dropdown-item" :class="{ 'text-muted': user.matched }" @click="matchUserSong(matchedSong, user)">{{ user.name }}</a>
                    </li>
                  </ul>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <!-- Submit song link -->
      <div class="row">
        <div class="col col-10 col-sm-6 offset-1 offset-sm-3">
          <div class="card px-0 mb-4">
            <div class="card-header">
              Submit next song
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col col-8 offset-2">
                  <input class="form-control" id="songInput" v-model="nextSong" required>
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
  name: 'Survey',
  props: {
    sotwId: String
  },
  data() {
    return {
      songs: [],
      users: [],
      userName: "",
      pickedSongs: [],
      matchedUserSongs: [],
      nextSong: "",
    };
  },
  computed: {
    
  },
  mounted() {
    const vm = this;
    // TODO make mock api calls using vuex
    vm.songs = [
      { id: 0, name: 'Good Will Hunting - Black Country, New Road' },
      { id: 1, name: 'Houdini - Dua Lipa' },
      { id: 2, name: 'Here Comes the Sun - The Beatles' },
    ];
    vm.users = [
      { id: 0, name: 'Jake', matched: false, },
      { id: 1, name: 'Joan', matched: false, },
      { id: 2, name: 'Daniel', matched: false, },
    ];
    vm.songs.forEach(e => {
      vm.matchedUserSongs.push({
        id: e.id,
        user: undefined,
        song: e,
      })
    });
  },
  methods: {
    matchUserSong(song, user) {
      const vm = this;
      // remove the user from any other matches it has
      vm.matchedUserSongs.forEach(e => {
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
    submitSurvey() {
      const vm = this;
      //TODO validation and form object creation
      let formData = {
        userName: vm.userName,
        pickedSongs: vm.pickedSongs,
        matchedUserSongs: vm.matchedUserSongs,
        nextSong: vm.nextSong,
      }
      console.log(formData);
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>
