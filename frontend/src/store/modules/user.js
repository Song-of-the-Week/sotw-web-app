import api from "@/shared/api";

export default {
  state: {
    user: null,
  },
  getters: {
    getUser: (state) => {
      return state.user;
    },
    isAuthenticated: (state) => {
      return !!state.user;
    },
  },
  actions: {
    async getCurrentUser({ commit }) {
      await api.methods
        .apiGetCurrentUser()
        .then(async (res) => {
          await commit("setUser", res.data);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    async logout({ commit }) {
      await api.methods
        .apiGetLogout()
        .then(async (res) => {
          await commit("setUser", null);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    async updateUser({ commit, state }, payload) {
      await api.methods
        .apiUpdateUser(state.user.id, payload)
        .then(async (res) => {
          await commit("setUser", res.data);
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
  },
};
