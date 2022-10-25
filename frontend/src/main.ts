import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import VueApexCharts from "vue3-apexcharts";
import naive from 'naive-ui'
import VueAxios from "vue-axios";
import axios from "axios";

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(naive)
app.use(VueApexCharts)
app.use(VueAxios, axios)

app.mount('#app')
