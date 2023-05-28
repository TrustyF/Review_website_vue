import {createRouter, createWebHistory} from "vue-router";

import MoviePage from "@/pages/MoviePage"
import MangaPage from "@/pages/MangaPage"
import SeriesPage from "@/pages/SeriesPage"

const router = createRouter({
    mode: 'history',
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "home",
            redirect: '/movies'
        },
        {
            path: "/movies",
            name: "movies",
            component: MoviePage
        },
        {
            path: "/series",
            name: "series",
            component: SeriesPage
        },
        {
            path: "/manga",
            name: "manga",
            component: MangaPage
        },
    ]
})

export default router