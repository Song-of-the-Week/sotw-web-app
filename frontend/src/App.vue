<template>
  <Navbar :sotwName="sotwName" />
  <router-view />
</template>

<script>
import { mapActions } from "vuex";
import Navbar from "./components/Navbar.vue";

export default {
  name: "App",
  components: {
    Navbar,
  },
  data() {
    return {
      sotwName: "Song of the Week",
      sotwId: 0,
    };
  },
  mounted() {
    const vm = this;

    // see if an active sotw has been set already
    const activeSotwId = localStorage.getItem("activeSotwId");
    if (activeSotwId !== null) {
      vm.getSotw(activeSotwId);
    }
  },
  methods: {
    ...mapActions(["getSotw"]),
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
./components/NavbarComponent.vue./components/Navbar.vue
