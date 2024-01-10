<template>
  <div class="home">
    <h1 class="mt-3">Welcome to {{ sotwName }}!</h1>
    <br/> 
    <h3>The survey will be released in:</h3>
    <br/>
    <Countdown/>
    <Survey/>
    <Results/>
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
  </div>
</template>

<script>
// @ is an alias to /src
import Countdown from '@/components/Countdown.vue'
import Survey from '@/components/Survey.vue'
import Results from '@/components/Results.vue'

export default {
  name: 'HomeView',
  components: {
    Countdown,
    Survey,
    Results,
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
