import Vue, {createApp, provide, inject} from 'vue'
import router from './router'
import App from './App'
import Popper from "vue3-popper";
import VueLazyload from "vue-lazyload";

const local_api = "http://localhost:5000"
const server_api = "https://trustyfox.pythonanywhere.com"

const app = createApp(App)

app.provide('curr_api', local_api)
app.use(router)
app.use(VueLazyload, {
    preLoad: 2,
    attempt: 2
})
app.mount('#app')