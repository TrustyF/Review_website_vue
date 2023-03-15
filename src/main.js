import Vue, {createApp} from 'vue'
import router from './router'
import App from './App'
import Popper from "vue3-popper";
import VueLazyload from "vue-lazyload";

const app = createApp(App)

app.component("PopperComp", Popper)
app.use(router)
app.use(VueLazyload, {
    preLoad: 2,
    attempt: 2
})
app.mount('#app')