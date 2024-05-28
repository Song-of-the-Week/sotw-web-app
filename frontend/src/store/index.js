import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import user from "./modules/user";
import sotw from "./modules/sotw";
import week from "./modules/week";

// create store
export default createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    user,
    sotw,
    week,
  },
  plugins: [createPersistedState()],
});
