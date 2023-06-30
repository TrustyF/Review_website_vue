import {createRouter, createWebHistory} from "vue-router";

import MoviePage from "@/pages/MoviePage"
import MangaPage from "@/pages/MangaPage"
import SeriesPage from "@/pages/SeriesPage"
import AnimePage from "@/pages/AnimePage"
import GamePage from "@/pages/GamePage"
import MoviePickerPage from "@/pages/MoviePickerPage";

const router = createRouter({
    mode: 'history',
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "home",
            redirect: '/movie_picker'
        },
        {
            path: "/movie_picker",
            name: "movie picker",
            component: MoviePickerPage
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
            path: "/anime",
            name: "anime",
            component: AnimePage
        },
        {
            path: "/manga",
            name: "manga",
            component: MangaPage
        },
        {
            path: "/games",
            name: "games",
            component: GamePage
        },
    ]
})

export default router