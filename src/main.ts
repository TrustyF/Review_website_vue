import {createApp, ref} from 'vue'
import router from './router/index'
import App from './App.vue'
// import Popper from "vue3-popper";
import VueLazyLoad from "vue-lazyload";

const local_api = "http://192.168.1.11:5000"
const server_api = "http://review-trustyfox.pythonanywhere.com/"
const devMode = import.meta.env.DEV
// const devMode = false
const editMode = ref(false)
const sessionSeed = Math.random()
const mediaRanges = ref(undefined)

const app = createApp(App)

app.provide('curr_api', devMode ? local_api : server_api)
app.provide('devMode', devMode)
app.provide('editMode', editMode)
app.provide('mediaRanges', mediaRanges)
app.provide('sessionSeed', sessionSeed)
app.provide('forceVis', ref(false))

app.use(VueLazyLoad, {
    preLoad: 2,
    attempt: 2
})
app.use(router)
app.mount('#app')
