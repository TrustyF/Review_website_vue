import {createRouter, createWebHistory} from "vue-router";

import HomePage from "../pages/HomePage.vue"
import InfoPage from "../pages/InfoPage.vue"
import MoviePage from "../pages/MoviePage.vue"
import MangaPage from "../pages/MangaPage.vue"
import SeriesPage from "../pages/SeriesPage.vue"
import ShortsPage from "../pages/ShortPage.vue"
import YoutubePage from "../pages/YoutubePage.vue"
import RiotPage from "../pages/sub_pages/youtube/YTRiotPage.vue"
import YTAnimationPage from "../pages/sub_pages/youtube/YTAnimationsPage.vue"
import YTShortPage from "../pages/sub_pages/youtube/YTShortsPage.vue"
import YTShowPage from "../pages/sub_pages/youtube/YTShowsPage.vue"
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
            path: "/info",
            name: "info",
            component: InfoPage,
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
            path: "/shorts",
            name: "shorts",
            component: ShortsPage
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
            path: "/youtube/yt_animations",
            name: "youtube animations",
            component: YTAnimationPage
        },
        {
            path: "/youtube/yt_short_films",
            name: "youtube short films",
            component: YTShortPage
        },
        {
            path: "/youtube/yt_shows",
            name: "youtube shows",
            component: YTShowPage
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