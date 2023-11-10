<template>
  <div class="home">
    <h1>Welcome to {{ sotwName }}!</h1>
    <br/>
    <h3>The survey will be released in:</h3>
    <br/>
    <Countdown/>
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
  </div>
</template>

<script>
// @ is an alias to /src
import Countdown from '@/components/Countdown.vue'

export default {
  name: 'HomeView',
  components: {
    Countdown
  },
  data() {
    return {
      sotwName: "Song of the Week",
      sotwId: 0,
      msg: "fuck off",
    };
  },
  methods: {

  },
}
</script>

<style scoped lang="scss">
.home {
  text-align: center;
}
</style>
