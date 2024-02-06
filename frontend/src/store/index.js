import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import user from "./modules/user";

// create store
export default createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    user,
  },
  plugins: [createPersistedState()],
});
