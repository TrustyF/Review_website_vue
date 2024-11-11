import {createRouter, createWebHistory} from "vue-router";
import {getAnalytics, logEvent} from "firebase/analytics";
import {log_event} from "@/scripts/log_events";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    scrollBehavior(to, from, savedPosition) {
        // return {top: 0}
    },
    routes: [
        {
            path: "/all",
            name: "all",
            component: () => import("../pages/AllPage.vue")
        },
        {
            path: "/",
            name: "home",
            component: () => import("../pages/HomePage.vue")
        },
        {
            path: "/info",
            name: "info",
            component: () => import("../pages/InfoPage.vue")
        },
        {
            path: "/movie",
            name: "movie",
            component: () => import("../pages/MoviePage.vue"),
        },
        {
            path: "/tv",
            name: "tv",
            component: () => import("../pages/SeriesPage.vue")
        },
        {
            path: "/movie_lists",
            name: "movie lists",
            component: () => import("../pages/sub_pages/movie_lists/MovieListsPage.vue")
        },
        {
            path: "/movie_lists/best_of_the_worst",
            name: "best of the worst",
            component: () => import("../pages/sub_pages/movie_lists/pages/BOTWPage.vue")
        },
        {
            path: "/movie_lists/shorts",
            name: "shorts",
            component: () => import("../pages/sub_pages/movie_lists/pages/ShortPage.vue")
        },
        {
            path: "/youtube",
            name: "youtube",
            component: () => import("../pages/sub_pages/youtube/YoutubePage.vue")
        },
        {
            path: "/youtube/riot_games_media",
            name: "riot games media",
            component: () => import("../pages/sub_pages/youtube/pages/YTRiotPage.vue")

        },
        {
            path: "/youtube/yt_animations",
            name: "youtube animations",
            component: () => import("../pages/sub_pages/youtube/pages/YTAnimationsPage.vue")
        },
        {
            path: "/youtube/yt_music_videos",
            name: "youtube music videos",
            component: () => import("../pages/sub_pages/youtube/pages/YTMusicVideoPage.vue")
        },
        {
            path: "/youtube/yt_short_films",
            name: "youtube short films",
            component: () => import("../pages/sub_pages/youtube/pages/YTShortsPage.vue")
        },
        {
            path: "/youtube/yt_anime_openings",
            name: "youtube anime openings",
            component: () => import("../pages/sub_pages/youtube/pages/YTAnimeOpeningPage.vue")
        },
        {
            path: "/youtube/yt_overwatch_cinematics",
            name: "youtube overwatch cinematics",
            component: () => import("../pages/sub_pages/youtube/pages/YTOverwatchPage.vue")
        },
        {
            path: "/youtube/yt_comedy",
            name: "youtube comedy",
            component: () => import("../pages/sub_pages/youtube/pages/YTComedyPage.vue")
        },
        {
            path: "/youtube/yt_documentaries",
            name: "youtube documentaries",
            component: () => import("../pages/sub_pages/youtube/pages/YTDocumentaryPage.vue")
        },
        {
            path: "/youtube/yt_essays",
            name: "youtube essays",
            component: () => import("../pages/sub_pages/youtube/pages/YTVideoEssayPage.vue")
        },
        {
            path: "/youtube/yt_shows",
            name: "youtube shows",
            component: () => import("../pages/sub_pages/youtube/pages/YTShowsPage.vue")
        },
        {
            path: "/youtube/youtube_debug",
            name: "youtube debug",
            component: () => import("../pages/sub_pages/youtube/pages/YoutubeDebug.vue")
        },
        {
            path: "/anime",
            name: "anime",
            component: () => import("../pages/AnimePage.vue")
        },
        {
            path: "/manga",
            name: "manga",
            component: () => import("../pages/MangaPage.vue")
        },
        {
            path: "/comic",
            name: "comic",
            component: () => import("../pages/ComicPage.vue")
        },
        {
            path: "/game",
            name: "game",
            component: () => import("../pages/GamePage.vue")
        },
        {
            path: "/pauline",
            name: "custom_pauline",
            component: () => import("../pages/custom_pages/PaulinePage.vue")
        },
    ],
})

router.beforeEach((to, from) => {
    // track page changes
    log_event('page_nav', 'nav', to.name)
})
export default router