import {createRouter, createWebHistory} from "vue-router";

import HomePage from '@/pages/HomePage'
import MangaPage from "@/pages/MangaPage";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "home",
            component: HomePage
        },
        {
            path: "/manga",
            name: "manga",
            component: MangaPage
        },
    ]
})

export default router