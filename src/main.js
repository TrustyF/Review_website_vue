import Vue, {createApp} from 'vue'
import router from './router'
import App from './App'
import Popper from "vue3-popper";
import VueLazyload from "vue-lazyload";

const app = createApp(App)

app.component("PopperComp", Popper)
app.use(router)
app.use(VueLazyload, {
    preLoad: 1.3,
    attempt: 1
})
app.mount('#app')