<template>
  <div class="container">
    <p>
      {{ timeLeft.days }} days {{ timeLeft.hours }} hours {{ timeLeft.minutes }} minutes {{ timeLeft.seconds }} seconds
    </p>
  </div>
</template>

<script>
export default {
  name: "Countdown",
  props: {
    releaseTimestamp: {
      type: Number,
      default: 0,
    },
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
      release: null,
    };
  },
  mounted() {
    const vm = this;

    vm.release = new Date(vm.releaseTimestamp);
    vm.getTimeRemaining();
    vm.countdownInterval = setInterval(vm.updateTimer, 1000);
  },
  methods: {
    getTimeRemaining() {
      const vm = this;
      let time = Date.parse(vm.release) - Date.parse(new Date());

      if (time >= 0) {
        vm.timeLeft.days = Math.floor(time / (1000 * 60 * 60 * 24));
        vm.timeLeft.hours = Math.floor((time / (1000 * 60 * 60)) % 24);
        vm.timeLeft.minutes = Math.floor((time / 1000 / 60) % 60);
        vm.timeLeft.seconds = Math.floor((time / 1000) % 60);
      } else {
        vm.timeLeft.days = vm.timeLeft.hours = vm.timeLeft.minutes = vm.timeLeft.seconds = 0;
      }
    },
    updateTimer() {
      const vm = this;

      if (vm.timeLeft.days > 0 || vm.timeLeft.hours > 0 || vm.timeLeft.minutes > 0 || vm.timeLeft.seconds > 0) {
        vm.getTimeRemaining();
      } else {
        // emit to parent that the countdown is over
        vm.$emit("counted-down");
        clearInterval(vm.countdownInterval);
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss"></style>
