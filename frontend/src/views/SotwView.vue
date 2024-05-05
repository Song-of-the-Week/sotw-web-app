<template>
  <div class="home">
    <h1 class="mt-3">Welcome to {{ sotwName }}!</h1>
    <div v-if="!sotw">
      <h2>Blah Blah Blah!</h2>
    </div>
    <div v-else>
      <br />
      <h3>The survey will be released in:</h3>
      <br />
      <Countdown />
      <Survey />
      <Results />
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import Countdown from "@/components/Countdown.vue";
import Survey from "@/components/Survey.vue";
import Results from "@/components/Results.vue";

export default {
  name: "SotwView",
  components: {
    Countdown,
    Survey,
    Results,
  },
  data() {
    return {
      sotwName: "Song of the Week",
    };
  },
  computed: {
    ...mapGetters({ sotw: "getActiveSotw" }),
  },
  mounted() {
    const vm = this;

    vm.getSotw(vm.$route.params.sotwId);
    localStorage.setItem("activeSotwId", vm.sotw.id);
  },
  methods: {
    ...mapActions(["getSotw"]),
  },
};
</script>

<style scoped lang="scss">
.home {
  text-align: center;
}
</style>
