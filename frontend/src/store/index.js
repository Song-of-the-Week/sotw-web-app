import { Vuex, createStore } from 'vuex'
import Vue from 'vue';
import createPersistedState from "vuex-persistedstate";
import auth from './modules/auth';

// create store
export default createStore({
  state: {
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    auth,
  },
  plugins: [
    createPersistedState(),
  ]
})
