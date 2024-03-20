<template>
  <div class="table-responsive">
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Name</th>
          <th scope="col">Playlist Link</th>
          <th scope="col">Survey Release Day and Time</th>
          <th scope="col">Results Release Day and Time</th>
          <th scope="col">Share Link</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sotw in sotwList">
          <td>{{ sotw.name }}</td>
          <td>
            <a :href="sotw.playlist_link" target="_blank">{{ sotw.playlist_link }}</a>
          </td>
          <td>{{ sotw.results }}</td>
          <td>{{ sotw.survey }}</td>
          <td>
            {{ sotw.share_link }}
            <button @click="copy(sotw.share_link)" class="btn btn-outline-secondary float-end">copy</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "SotwTable",
  props: {
    sotwList: Array,
  },
  data() {
    return {};
  },
  mounted() {},
  methods: {
    copy(link) {
      navigator.clipboard.writeText(link);
    },
  },
};
</script>

<style scoped lang="scss"></style>
