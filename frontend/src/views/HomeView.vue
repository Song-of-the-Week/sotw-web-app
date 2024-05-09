<template>
  <div class="row">
    <div class="col">
      <h1 class="mt-3">Welcome to Song of the Week!</h1>
      <div v-if="!isLoggedIn">
        <h2>What is Song of the Week?</h2>
        <p>
          Song of the Week is meant to be a friendly competition where you and your friends can finally determine who
          has the best music taste through democracy! I guess this also allows you to introduce your friends to new
          music and learn more about them as you go along, creating a deeper understanding and connection between you
          forming a bond that will last lifetimes, but it's mostly about winning.
        </p>
        <h3>How does the competition work?</h3>
        <p>
          Every week, you and whoever else is a part of your Song of the Week competition submit a song anonymously.
          Once everyone has submitted a song, a Spotify playlist composed of everyone's submission is created and made
          available to everyone in the competition. Over the course of the next week, you and your friends will listen
          to the playlist until the next survey is released on a scheduled day and time. The survey will have you pick
          your favorite two songs from the playlist that week (votes for your own song are not counted for that song),
          match each of the players in the competition with one of the songs in the playlist, and submit a new song for
          next week's playlist. The results of the survey will be shown on a scheduled day and time once everyone has
          submitted a response and it will show everyone which song(s) got the most votes, which players got the most
          and least correct matches, and a breakdown of who voted for which song and who made each guess. The top voted
          songs will be added to a Song of the Year playlist available to everyone. The next playlist will also be
          released along with the results of the previous week's survey and thus, the circle of Song of the Week
          continues.
        </p>

        <p>
          Anyway, it looks like you're not logged in. Please
          <router-link :to="`/login`"><a class="">login</a></router-link> or
          <router-link :to="`/register`"><a class="">register</a></router-link> to enter or start your own Song of the
          Week competition!
        </p>
      </div>
      <div v-else class="text-center">
        <div v-if="user.sotw_list.length == 0">
          <h2>
            It looks like you are not a part of any Song of the Week competitions :( You can create one by clicking the
            button below, or you can join one by clicking on a share link that a friend sends you.
          </h2>
        </div>
        <div v-else>
          <h2>Choose a Song of the Week to enter or create a new one!</h2>
          <div class="row">
            <div class="col"></div>
            <div class="col-10 col-lg-3 p-4">
              <div class="list-group">
                <router-link
                  v-for="sotw in user.sotw_list"
                  class="list-group-item list-group-item-action"
                  :to="`/sotw/` + sotw.id"
                  >{{ sotw.name }}</router-link
                >
              </div>
            </div>
            <div class="col"></div>
          </div>
        </div>
        <button class="btn btn-outline-success" @click="create()">Create</button>
      </div>
    </div>
  </div>
  <SotwCreationModal v-if="isLoggedIn" :sotw-creation-modal="sotwCreationModal" />
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import store from "@/store/index.js";
import SotwCreationModal from "@/components/SotwCreationModal.vue";

export default {
  name: "HomeView",
  components: {
    SotwCreationModal,
  },
  data() {
    return {
      sotwCreationModal: null,
    };
  },
  computed: {
    ...mapGetters({ sotw: "getActiveSotw", user: "getUser" }),
    isLoggedIn: () => {
      return store.getters.isAuthenticated;
    },
  },
  mounted() {
    const vm = this;

    if (vm.isLoggedIn) {
      vm.sotwCreationModal = new window.bootstrap.Modal("#sotwCreationModal");
    }
  },
  methods: {
    ...mapActions(["getSotw"]),
    create() {
      const vm = this;
      if (!vm.sotwCreationModal._isShown) {
        vm.sotwCreationModal.show();
      }
    },
  },
};
</script>

<style scoped lang="scss">
.home {
  text-align: center;
}
</style>
