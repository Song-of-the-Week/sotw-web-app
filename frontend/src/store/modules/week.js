import api from "@/shared/api";

export default {
  state: {
    currentWeek: null,
    currentWeekError: null,
  },
  getters: {
    getCurrentWeek: (state) => {
      return state.currentWeek;
    },
    getCurrentWeekError: (state) => {
      return state.currentWeekError;
    },
  },
  actions: {
    async getWeek({ commit }, id) {
      await api.methods
        .apiGetWeek(id)
        .then(async (res) => {
          if ("status" in res.data && "message" in res.data && "week" in res.data) {
            await commit("setCurrentWeekError", res.data.message);
            await commit("setCurrentWeek", res.data.week);
          } else {
            await commit("setCurrentWeekError", null);
            await commit("setCurrentWeek", res.data);
          }
        })
        .catch((err) => {
          // localStorage.removeItem("activeSotwId");
        });
    },
  },
  mutations: {
    setCurrentWeek(state, week) {
      state.currentWeek = week;
    },
    setCurrentWeekError(state, err) {
      state.currentWeekError = err;
    },
  },
};
