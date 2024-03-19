import {createApp, ref, defineComponent, provide} from 'vue'
import router from './router/index'
import App from './App.vue'

import VueLazyLoad from "vue-lazyload";
import {initializeApp} from 'firebase/app';
import axiosRetry from 'axios-retry';
import axios from 'axios';

const local_api = "http://192.168.1.11:5000"
const server_api = "https://review-trustyfox.pythonanywhere.com"

// const devMode = import.meta.env.DEV
const devMode = false

const edit_mode = ref(false)

const session_seed = Math.round(Math.random() * 100)
const firebaseConfig = {
    apiKey: "AIzaSyCiUSfDjsau5Xa0lGRfPDxOnFePhr64yY0",
    authDomain: "vue-review-website.firebaseapp.com",
    projectId: "vue-review-website",
    storageBucket: "vue-review-website.appspot.com",
    messagingSenderId: "832888321299",
    appId: "1:832888321299:web:7a93c03b654f01516d56e6"
};

initializeApp(firebaseConfig);
const app = createApp(App)

app.provide('curr_api', devMode ? local_api : server_api)
app.provide('devMode', devMode)
app.provide('edit_mode', edit_mode)
app.provide('session_seed', session_seed)

//tooltips
app.provide('tooltip_badge_hover', ref(false))
app.provide('tooltip_badge_pos', ref([0, 0]))
app.provide('tooltip_badge_data', ref({}))

axiosRetry(axios, {
    retryDelay: ((count) => count * 200),
    retries: 50,
    onRetry: ((retryCount,error) => console.log('retry',retryCount,error.message,error.code)),
    retryCondition: ((error) => {
        return true
    })
});

app.use(VueLazyLoad, {
    preLoad: 0,
    attempt: 10,
    observer: true,
    throttleWait: 1000,
})
app.directive('v-lazy')
app.use(router)
app.mount('#app')
