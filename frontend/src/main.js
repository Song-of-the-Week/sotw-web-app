import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import config from "./shared/config";
import axios from "axios";

/* axios config */
axios.defaults.withCredentials = true;
axios.defaults.baseURL = config.API_HOSTNAME;
axios.interceptors.response.use(undefined, function (error) {
  if (error) {
    console.log("HUH", error);
    const status = error.response !== undefined ? error.response.status : 500;
    const originalRequest = error.config;
    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      store.dispatch("logout");
      return router.push("/login");
    } else if (status === 404) {
      return router.push("/404");
    } else if (status == 403) {
      return router.push("/403");
    } else {
      return Promise.reject(error);
    }
  }
});

/* import bootstrap styles */
import "bootstrap/dist/css/bootstrap.css";

/* import bootstrap-icons styles */
import "bootstrap-icons/font/bootstrap-icons.css";

/* import vue-charts from canvasjs */
import CanvasJSChart from "@canvasjs/vue-charts";

/* import vue-cookies */
import VueCookies from "vue-cookies";

/* define window level variables */
window.$ = window.jQuery = require("jquery");
window.bootstrap = require("bootstrap/dist/js/bootstrap.bundle.js");
window.config = config;

createApp(App).use(store).use(router).use(CanvasJSChart).use(VueCookies).mount("#app");
