import Vue, {createApp} from 'vue'
import router from './router'
import App from './App'
import Popper from "vue3-popper";

const app = createApp(App)
app.component("PopperComp", Popper)
app.use(router)
app.mount('#app')