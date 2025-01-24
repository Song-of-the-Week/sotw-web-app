<template>
      <CContainer class="mb-4">
      <div class="w-50 mx-auto mb-4">
      <h1 class="mt-3">Welcome to Song of the Week!</h1>
      </div>
      </CContainer>
      <div v-if="!isLoggedIn">
        <CContainer class="mb-4">
          <div class="w-50 mx-auto mb-4">
          <CCard>
            <CCardBody>
              <CCardTitle>It looks like you aren't signed in</CCardTitle>
              <CCardSubtitle class="mb-2 text-body-secondary">Please sign in or register to use Song of the Week</CCardSubtitle>
              <router-link :to="`/login`">
                <CButton color="primary" class="me-2">Login</CButton>
              </router-link>
              <router-link :to="`/register`">
                <CButton color="secondary" class="me-2">Register</CButton>
              </router-link>
            </CCardBody>
          </CCard>
          </div>
        </CContainer>
        <CContainer class="mb-4">
          <div class="w-75 mx-auto mb-4">
          <CAccordion>
            <CAccordionItem :item-key="1">
              <CAccordionHeader>
                What is Song of the Week?
              </CAccordionHeader>
              <CAccordionBody>
                <p>
                  Song of the Week is meant to be a friendly competition where you and your friends can finally
                  determine who
                  has the best music taste through democracy!</p>
                <p>
                  It allows you to introduce your friends to new
                  music and learn more about them as you go along, creating a deeper understanding and connection
                  between you,
                  forming a bond that will last lifetimes or something, but it's mostly about winning.
                </p>
              </CAccordionBody>
            </CAccordionItem>
            <CAccordionItem :item-key="2">
              <CAccordionHeader>
                How Does It Work?
              </CAccordionHeader>
              <CAccordionBody>
                <p>
                  Every week, you and whoever else is a part of your Song of the Week competition submit a song
                  anonymously in a
                  survey. Once everyone has submitted a song, a Spotify playlist composed of everyone's submission is
                  created
                  and made available to everyone in the competition.
                </p>
                <p>
                  Over the course of the next week, you and your friends will listen to the playlist and fill out the
                  next survey before the week ends. Each survey (except for the very
                  first one) will have you pick your favorite two songs from the playlist that week (votes for your own
                  song are
                  not counted for that song), match each of the players in the competition with one of the songs in the
                  playlist, and submit a new song for next week's playlist.
                </p>

                <p>
                  The results of the previous week's survey will be
                  shown on a day chosen by the Song of the Week competition creator. Once everyone has submitted a
                  response and you will see
                  song(s) got the most votes, which players got the most and least correct matches, and a breakdown of
                  who voted
                  for which song and who made each guess. The top voted song(s) each week will be added to a Song of the
                  Year
                  playlist available to everyone. The next playlist and a new survey will also be released with the
                  previous
                  week's results, and thus, the circle of Song of the Week continues.
                </p>
              </CAccordionBody>
            </CAccordionItem>
            <CAccordionItem :item-key="3">
              <CAccordionHeader>
                How Many Songs Win Each Week?
              </CAccordionHeader>
              <CAccordionBody>
                <p>
                  The top two songs every week will win, unless there are ties. If there are ties for first, all songs
                  tied for first will make the
                  Song of the Year playlist, and no second place songs will be added. Likewise, if one song receives the
                  most votes but there is a tie
                  for second, all second place songs will make the Song of the Year.
                </p>
              </CAccordionBody>
            </CAccordionItem>

            <CAccordionItem :item-key="4">
              <CAccordionHeader>
                Do I Need A Spotify Account?
              </CAccordionHeader>
              <CAccordionBody>
                <p>
                  Yes. In addition, you must make sure your account is linked before attempting to join a Song of the
                  Week competition.
                </p>
              </CAccordionBody>
            </CAccordionItem>
          </CAccordion>
          </div>
        </CContainer>

        <h2></h2>
        <p>
        </p>
        <h3></h3>
        <p>

        </p>

        <p>
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
                <router-link v-for="sotw in user.sotw_list" class="list-group-item list-group-item-action"
                  :to="`/sotw/` + sotw.id">{{ sotw.name }}</router-link>
              </div>
            </div>
            <div class="col"></div>
          </div>
        </div>
        <router-link to="/sotw/create">
          <button class="btn btn-outline-success" @click="create()">Create</button>
        </router-link>
      </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import api from "@/shared/api";
import store from "@/store/index.js";
import {
  CAccordion,
  CAccordionItem,
  CAccordionBody,
  CButton,
  CAccordionHeader,
  CContainer,
  CCard,
  CCardBody,
  CCardTitle,
  CCardSubtitle,
} from '@coreui/vue';

export default {
  name: "HomeView",
  components: {
    CAccordion,
    CAccordionItem,
    CAccordionBody,
    CButton,
    CAccordionHeader,
    CContainer,
  CCard,
  CCardBody,
  CCardTitle,
  CCardSubtitle,
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
  async mounted() {
    const vm = this;

    // check for redirection from spotify
    await vm.$router.isReady().then((_) => {
      if ("state" in vm.$route.query && vm.$route.query.state == vm.user.email + "-" + vm.user.name.replace(/\s+/g, '-')) {
        if ("code" in vm.$route.query) {
          const payload = {
            code: vm.$route.query.code,
            state: vm.$route.query.state,
          };
          // make api call to backend with the authorization code and update user on front end
          api.methods
            .apiUpdateUserSpotifyToken(payload)
            .then(async (res) => {
              await vm.getCurrentUser();
            })
            .then((_) => {
              vm.$router.push(sessionStorage.getItem("last_requested_path"));
            });
          // TODO maybe add toastr or modal or something to indicate spotify linked
        } else if ("error" in vm.$route.query) {
          console.log("ERROR", vm.$route.query.error);
          // TODO maybe add toastr or something to indicate spotify not linked
        }
      } else if (vm.$route.name == "verify") {
        // make api call to backend to verify the token and update user on front end
        api.methods
          .apiGetVerifyRegistration(vm.$route.params.verificationToken)
          .then(async (res) => {
            await vm.getCurrentUser();
          })
          .then((_) => {
            vm.$router.push("/link-spotify");
          })
          .catch((err) => {
            console.error("Invalid link:", err);
          });
      }

      vm.loginRegisterModal = new window.bootstrap.Modal("#loginModal");
      if (vm.isLoggedIn) {
        vm.sotwCreationModal = new window.bootstrap.Modal("#sotwCreationModal");
      }
    });
  },
  methods: {
    ...mapActions(["getSotw", "getCurrentUser"]),
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
