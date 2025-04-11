import { createApp } from 'vue/dist/vue.esm-bundler'
import App from "./App.vue";
import router from "./router";
import store from "./store";
import config from "./shared/config";
import axios from "axios";

// Axios config
axios.defaults.withCredentials = true;
axios.defaults.baseURL = config.API_HOSTNAME;
axios.interceptors.response.use(undefined, (error) => {
  if (error) {
    const status = error.response !== undefined ? error.response.status : 500;
    const originalRequest = error.config;
    if (status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      store.dispatch("logout");
      return router.push("/login");
    } else if (status === 404 && originalRequest.url != "api/v1/user/reset-password") {
      return router.push("/404");
    } else if (status == 403 && !originalRequest.url.startsWith("api/v1/sotw/invite/pending/")) {
      return router.push("/403");
    } else {
      return Promise.reject(error);
    }
  }
});

// Import Bootstrap CSS
import "bootstrap/dist/css/bootstrap.css";

// Import Bootstrap Icons
import "bootstrap-icons/font/bootstrap-icons.css";

// Import CanvasJS Chart for Vue
import CanvasJSChart from "@canvasjs/vue-charts";

// Import Vue-Cookies
import VueCookies from "vue-cookies";

// Set window-level variables
window.config = config;

// Make jQuery and Bootstrap accessible globally via the window object
import "bootstrap/dist/js/bootstrap.bundle.min.js"; // Vite handles this optimally via ES modules
import $ from "jquery"; // Import jQuery via ES modules
import * as bootstrap from "bootstrap";

window.$ = $;
window.jQuery = $;
window.bootstrap = window.bootstrap || bootstrap;

// Create the Vue app and mount it
createApp(App)
  .use(store)
  .use(router)
  .use(CanvasJSChart)
  .use(VueCookies)
  .mount("#app");
