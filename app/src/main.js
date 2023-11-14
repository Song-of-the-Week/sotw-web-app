import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

/* import bootstrap styles */
import 'bootstrap/dist/css/bootstrap.css';

/* import bootstrap-icons styles */
import 'bootstrap-icons/font/bootstrap-icons.css';

/* import vue-charts from canvasjs */
import CanvasJSChart from '@canvasjs/vue-charts';

createApp(App).use(store).use(router).use(CanvasJSChart).mount('#app');

/* import bootstrap scripts */
import 'bootstrap/dist/js/bootstrap.js';