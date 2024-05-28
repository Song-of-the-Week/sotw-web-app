import api from "@/shared/api";

export default {
  state: {
    currentWeek: null,
  },
  getters: {
    getCurrentWeek: (state) => {
      return state.currentWeek;
    },
  },
  actions: {
    async getWeek({ commit }, id) {
      await api.methods
        .apiGetWeek(id)
        .then(async (res) => {
          await commit("setCurrentWeek", res.data);
        })
        .catch((err) => {
          localStorage.removeItem("activeSotwId");
        });
    },
    async submitSurvey(sotwId, weekNum, payload) {
      await api.methods.apiPostSurveyResponse(sotwId, weekNum, payload);
    },
  },
  mutations: {
    setCurrentWeek(state, week) {
      state.currentWeek = week;
    },
  },
};
