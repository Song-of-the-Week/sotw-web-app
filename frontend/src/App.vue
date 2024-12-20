<template>
  <Navbar />
  <div class="container-fluid">
    <router-view />
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import store from "@/store/index.js";
import Navbar from "./components/Navbar.vue";

export default {
  name: "App",
  components: {
    Navbar,
  },
  computed: {
    isLoggedIn: () => {
      return store.getters.isAuthenticated;
    },
  },
  mounted() {
    const vm = this;

    // see if an active sotw has been set already
    // const activeSotwId = localStorage.getItem("activeSotwId");
    // if (activeSotwId !== null && vm.isLoggedIn) {
    //   vm.getSotw(activeSotwId);
    // }
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
