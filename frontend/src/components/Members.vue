<template>
  <div class="container">
    <h2>Members</h2>
    <div v-if="loading" class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <ul v-else class="list-group">
      <li v-for="member in members" :key="member.id" class="list-group-item">
        {{ member.name }}
      </li>
    </ul>
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
  async created() {
    try {
      const sotwId = this.$route.params.sotwId;
      const response = await api.methods.apiGetSotwMembers(sotwId);
      this.members = response.data;
    } catch (error) {
      console.error('Error fetching members:', error);
    } finally {
      this.loading = false;
    }
  }
}
</script>