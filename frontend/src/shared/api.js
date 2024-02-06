import axios from "axios";

export default {
  methods: {
    apiGetHello() {
      return axios.get("");
    },
    apiPostRegister(form) {
      return axios.post(config.BASE_API_V1_URL + "auth/register", form);
    },
    apiPostLogin(form) {
      return axios.post(config.BASE_API_V1_URL + "auth/login", form);
    },
    apiGetLogout() {
      return axios.get(config.BASE_API_V1_URL + "auth/logout");
    },
    apiGetCurrentUser() {
      return axios.get(config.BASE_API_V1_URL + "auth/current_user");
    },
    apiUpdateUser(id, payload) {
      return axios.put(config.BASE_API_V1_URL + "user/" + id, payload);
    },
  },
};
