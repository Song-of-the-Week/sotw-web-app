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
    async register({ dispatch }, form) {
      await api.methods
        .apiPostRegister(form)
        .then(async (res) => {
          console.log("register", res, form);
          if (res.status == 201) {
            dispatch("login", form);
          }
          // let userForm = new FormData();
          // userForm.append("username", form.username);
          // userForm.append("password", form.password);
          // await axios.post("login", userForm);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async login({ commit }, form) {
      await api.methods
        .apiPostLogin({ username: form.email, password: form.password })
        .then(async (res) => {
          console.log("login", res);
          commit("setUser", user);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async logout({ commit }) {
      await commit("logout");
    },
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    logout(state) {
      state.user = null;
    },
  },
};
