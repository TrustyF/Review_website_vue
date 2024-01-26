import {createApp, ref, defineComponent} from 'vue'
import router from './router/index'
import App from './App.vue'

import VueLazyLoad from "vue-lazyload";

const local_api = "http://192.168.1.11:5000"
const server_api = "https://review-trustyfox.pythonanywhere.com/"

const devMode = import.meta.env.DEV
// const devMode = false
// const edit_mode = import.meta.env.DEV
const edit_mode = false

const session_seed = Math.round(Math.random() * 100)

const app = createApp(App)

app.provide('curr_api', devMode ? local_api : server_api)
app.provide('devMode', devMode)
app.provide('edit_mode', edit_mode)
app.provide('session_seed', session_seed)

//tooltips
app.provide('tooltip_badge_hover', ref(false))
app.provide('tooltip_badge_pos', ref([0,0]))
app.provide('tooltip_badge_data', ref({}))

app.use(VueLazyLoad, {
    preLoad: 2,
    attempt: 2,
})
app.directive('v-lazy')
app.use(router)
app.mount('#app')
