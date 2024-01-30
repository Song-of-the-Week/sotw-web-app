import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import config from "./shared/config";
import axios from "axios";

/* axios config */
axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://localhost:8000/";
axios.interceptors.response.use(undefined, function (error) {
  if (error) {
    const status = error.response.status;
    const originalRequest = error.config;
    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      store.dispatch("logout");
      return router.push("/login");
    } else if (status === 404) {
      return router.push("/404");
    }
  }
});

/* import bootstrap styles */
import "bootstrap/dist/css/bootstrap.css";

/* import bootstrap-icons styles */
import "bootstrap-icons/font/bootstrap-icons.css";

/* import vue-charts from canvasjs */
import CanvasJSChart from "@canvasjs/vue-charts";

/* define window level variables */
window.$ = window.jQuery = require("jquery");
window.bootstrap = require("bootstrap/dist/js/bootstrap.bundle.js");
window.config = config;

createApp(App).use(store).use(router).use(CanvasJSChart).mount("#app");
