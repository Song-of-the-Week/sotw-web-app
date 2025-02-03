<template>
  <div class="container">
    <div v-if="loading" class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <div v-else class="d-flex justify-content-center">
      <div class="card" style="width: 30rem;">
        <div class="card-header">
          Members
        </div>
        <div class="card-body">
          <table class="table">
            <thead>
              <tr>
                <th scope="col">Name</th>
                <th scope="col">Playlist</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="member in sortedMembers" :key="member.id">
                <td>{{ member.name }}</td>
                <td>
                  <a :href="member.playlistLink" target="_blank" class="btn btn-primary">
                    <i class="bi bi-spotify me-2"></i>
                    View on Spotify
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/shared/api'

export default {
  name: 'Members',
  data() {
    return {
      members: [],
      loading: true
    }
  },
  computed: {
    sortedMembers() {
      return this.members.sort((a, b) => a.name.localeCompare(b.name));
    }
  },
  async created() {
    try {
      const sotwId = this.$route.params.sotwId;
      const response = await api.methods.apiGetSotwMembers(sotwId);
      this.members = response.data.map(member => ({
        ...member,
        playlistLink: member.playlists.length > 0 ? member.playlists[0].playlist_link : '#'
      }));
    } catch (error) {
      console.error('Error fetching members:', error);
    } finally {
      this.loading = false;
    }
  }
}
</script>