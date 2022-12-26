import {createApp} from 'vue'
import {createPinia} from 'pinia'

import App from './App.vue'
import router from './router'

// import VueApexCharts from "vue3-apexcharts";
import VueAxios from "vue-axios";
import axios from "axios";

//@ts-ignore
import Ripple from "./directives/ripple"
Ripple.color = 'rgba(255, 255, 255, 0.35)';

//@ts-ignore
import Vuesax from 'vuesax3'
import 'vuesax3/dist/vuesax.css'
import 'material-icons/iconfont/material-icons.css';

import Vue3TouchEvents from "vue3-touch-events";

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(Vue3TouchEvents);
app.use(VueAxios, axios)
app.use(Vuesax, {})
// app.use(VueApexCharts)
app.directive('ripple', Ripple)

app.mount('#app')
