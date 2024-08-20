<template>
  <iframe
    style="border-radius: 12px"
    :src="embedSpotifyLink"
    width="100%"
    height="100%"
    frameBorder="0"
    allowfullscreen=""
    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
    loading="lazy"
  ></iframe>
</template>

<script>
export default {
  name: "SpotifyEmbed",
  props: {
    spotifyLink: {
      type: String,
      default: "",
    },
    type: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      embedSpotifyLink: "",
    };
  },
  mounted() {
    const vm = this;

    let spotifyId = vm.spotifyLink.split("/").pop().split("?")[0];

    vm.embedSpotifyLink = "https://open.spotify.com/embed/" + vm.type + "/" + spotifyId;
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
