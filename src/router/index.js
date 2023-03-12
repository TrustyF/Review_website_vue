import {createRouter, createWebHistory} from "vue-router";

import HomePage from '@/pages/HomePage'
import DbHelper from "@/pages/DbHelper"

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "home",
            component: HomePage
        },
        // {
        //     path: "/helper",
        //     name: "helper",
        //     component: DbHelper
        // }
    ]
})

export default router