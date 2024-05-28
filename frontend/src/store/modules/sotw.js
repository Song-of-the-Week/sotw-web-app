import api from "@/shared/api";

export default {
  state: {
    activeSotw: null,
  },
  getters: {
    getActiveSotw: (state) => {
      return state.activeSotw;
    },
  },
  actions: {
    async getSotw({ commit, dispatch }, id) {
      await api.methods
        .apiGetSotw(id)
        .then(async (res) => {
          await commit("setActiveSotw", res.data);
        })
        .then(async (res) => {
          await dispatch("getWeek", id, { root: true });
        })
        .catch((err) => {
          localStorage.removeItem("activeSotwId");
        });
    },
    async createSotw({ commit }, payload) {
      await api.methods
        .apiPostSotw(payload)
        .then(async (res) => {
          await commit("setActiveSotw", res.data);
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  mutations: {
    setActiveSotw(state, sotw) {
      state.activeSotw = sotw;
    },
  },
};
