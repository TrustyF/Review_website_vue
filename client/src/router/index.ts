import {createRouter, createWebHistory} from "vue-router";

import HomePage from "../pages/HomePage.vue"
import MoviePage from "../pages/MoviePage.vue"
import MangaPage from "../pages/MangaPage.vue"
import SeriesPage from "../pages/SeriesPage.vue"
import YoutubePage from "../pages/YoutubePage.vue"
import RiotPage from "../pages/sub_pages/youtube/RiotPage.vue"
import YTDebugPage from "../pages/sub_pages/youtube/YoutubeDebug.vue"

import AnimePage from "../pages/AnimePage.vue"
import GamePage from "../pages/GamePage.vue"
import AllPage from "../pages/AllPage.vue"

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/all",
            name: "all",
            component: AllPage
        },
        {
            path: "/",
            name: "home",
            component: HomePage,
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
            path: "/youtube",
            name: "youtube",
            component: YoutubePage
        },
        {
            path: "/youtube/riot_games_media",
            name: "riot games media",
            component: RiotPage
        },
        {
            path: "/youtube/youtube_debug",
            name: "youtube debug",
            component: YTDebugPage
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