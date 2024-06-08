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
          throw new Error(err.response.data.detail, { cause: err.response.status });
        });
    },
  },
  mutations: {
    setActiveSotw(state, sotw) {
      state.activeSotw = sotw;
    },
  },
};
