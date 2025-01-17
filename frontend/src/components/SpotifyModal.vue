<template>
  <div class="modal fade" id="spotifyModal" tabindex="-1" role="dialog" aria-labelby="spotifyModal" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Link Your Spotify Account</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>
            In order to participate in any Song of the Week competitions, please link your Spotify account by pressing
            the button below.
          </p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="linkSpotify()">Link</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import api from "@/shared/api";
export default {
  name: "SpotifyModal",
  props: {
    alertModal: {
      default: null,
    },
  },
  computed: {
    ...mapGetters({
      user: "getUser",
    }),
  },
  methods: {
    async linkSpotify() {
      const vm = this;
      await api.methods.getSpotifyClientId().then((res) => {
        let params = new URLSearchParams({
          client_id: res.data.client_id,
          response_type: "code",
          redirect_uri: config.SPOTIFY_CALLBACK_URI,
          state: vm.user.email + "-" + vm.user.name.replace(/\s+/g, '-'),
          scope: "playlist-modify-public",
        });
        document.location = `https://accounts.spotify.com/authorize?${params.toString()}`;
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
</style>
