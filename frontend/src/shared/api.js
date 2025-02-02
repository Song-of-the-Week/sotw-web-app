import axios from "axios";
import config from "./config";

export default {
  methods: {
    apiGetHello() {
      return axios.get("");
    },
    getSpotifyClientId() {
      return axios.get(config.BASE_API_V1_URL + "auth/spotify-client-id");
    },
    // USER
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
    apiUpdateUserSpotifyToken(payload) {
      return axios.put(config.BASE_API_V1_URL + "auth/spotify-access-token", payload);
    },
    apiGetVerifyRegistration(verificationToken) {
      return axios.get(config.BASE_API_V1_URL + "auth/verify/" + verificationToken);
    },
    apiGetVerifyEmail(verificationToken) {
      return axios.get(config.BASE_API_V1_URL + "user/verify/" + verificationToken);
    },
    apiPostResetPassword(payload) {
      return axios.post(config.BASE_API_V1_URL + "user/reset-password", payload);
    },
    apiPostResetPasswordChange(payload, verificationToken) {
      return axios.post(config.BASE_API_V1_URL + "user/reset-password-change/" + verificationToken, payload);
    },
    // SOTW
    apiPostSotw(payload) {
      return axios.post(config.BASE_API_V1_URL + "sotw/", payload);
    },
    apiGetSotw(id) {
      return axios.get(config.BASE_API_V1_URL + "sotw/" + id);
    },
    apiGetSotwInviteLink(id) {
      return axios.get(config.BASE_API_V1_URL + "sotw/" + id + "/invite");
    },
    apiGetSotwInvitePending(shareToken) {
      return axios.get(config.BASE_API_V1_URL + "sotw/invite/pending/" + shareToken);
    },
    apiGetSotwInviteJoin(shareToken) {
      return axios.get(config.BASE_API_V1_URL + "sotw/invite/join/" + shareToken);
    },
    apiGetSotwMembers(sotwId) {
      return axios.get(config.BASE_API_V1_URL + "sotw/" + sotwId + "/members");
    },
    apiGetLeaveSotw(sotwId) {
      return axios.get(config.BASE_API_V1_URL + "sotw/" + sotwId + "/leave");
    },
    apiGetSotwResponse(sotwId, userId) {
      return axios.get(config.BASE_API_V1_URL + "response/" + sotwId + "/" + userId);
    },
    // WEEK
    apiGetWeek(id) {
      return axios.get(config.BASE_API_V1_URL + "week/" + id + "/current_week");
    },
    // RESPONSE
    apiPostSurveyResponse(sotwId, weekNum, payload) {
      return axios.post(config.BASE_API_V1_URL + "response/" + sotwId + "/" + weekNum, payload);
    },
    // RESULTS
    apiGetResults(sotwId, weekNum) {
      return axios.get(config.BASE_API_V1_URL + "results/" + sotwId + "/" + weekNum);
    },
  },
};
