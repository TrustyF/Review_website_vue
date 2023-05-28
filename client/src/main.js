import Vue, {createApp, provide, inject,ref} from 'vue'
import router from './router'
import App from './App'
import Popper from "vue3-popper";
import VueLazyload from "vue-lazyload";

const local_api = "http://localhost:5000"
const server_api = "https://trustyfox.pythonanywhere.com"
let devMode = false
let darkMode = ref(true)
let sessionSeed = Math.random()


const app = createApp(App)

app.provide('curr_api', devMode ? local_api : server_api)
app.provide('devMode', devMode)
app.provide('darkMode', darkMode)
app.provide('sessionSeed', sessionSeed)

app.use(VueLazyload, {
    preLoad: 2,
    attempt: 2
})
app.use(router)
app.mount('#app')