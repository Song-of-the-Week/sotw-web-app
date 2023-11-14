<template>
  <div>
    <p>{{ timeLeft.days }} days {{ timeLeft.hours }} hours {{ timeLeft.minutes }} minutes {{ timeLeft.seconds }} seconds</p>
  </div>
</template>

<script>
 export default {
  name: 'Countdown',
  props: {
    sotwId: String
  },
  data() {
    return {
      timeLeft: {
        days: 0,
        hours: 0,
        minutes: 0,
        seconds: 0,
      },
      countdownInterval: undefined,
    };
  },
  computed: {
    release: function() {
      const vm = this;
      // TODO get the sotw survey release time (expect it as a datetime object froom the back end)
      let release = new Date(2023, 10, 10, 21, 0, 0, 0);
      return release;
    }
  },
  mounted() {
    const vm = this;
    vm.getTimeRemaining();
    vm.countdownInterval = setInterval(vm.updateTimer, 1000);
  },
  methods: {
    getTimeRemaining() {
      const vm = this;
      let time = Date.parse(vm.release) - Date.parse(new Date());
      console.log('hey');

      if (time >= 0) {
        vm.timeLeft.days = Math.floor(time / (1000 * 60 * 60 * 24));
        vm.timeLeft.hours = Math.floor(time / (1000 * 60 * 60) % 24);
        vm.timeLeft.minutes = Math.floor(time / 1000 / 60 % 60);
        vm.timeLeft.seconds = Math.floor(time / 1000 % 60);
      } else {
        vm.timeLeft.days = vm.timeLeft.hours = vm.timeLeft.minutes = vm.timeLeft.seconds = 0;
      }
    },
    updateTimer() {
      const vm = this;

      if (vm.timeLeft.days > 0 || vm.timeLeft.hours > 0 || vm.timeLeft.minutes > 0 || vm.timeLeft.seconds > 0) {
        vm.getTimeRemaining();
      } else {
        console.log('bang')
        clearInterval(vm.countdownInterval);
      }
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>
