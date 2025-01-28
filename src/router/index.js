import {createRouter, createWebHistory} from "vue-router";
import {log_event} from "@/scripts/log_events";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    scrollBehavior(to, from, savedPosition) {
        return {top: 0}
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
            name: "movie_lists_home",
            children: [
                {
                    path: '',
                    name: 'movie_lists',
                    component: () => import("../pages/sub_pages/movie_lists/MovieListsPage.vue")
                },
                {
                    path: "best_of_the_worst",
                    name: "best of the worst",
                    component: () => import("../pages/sub_pages/movie_lists/pages/BOTWPage.vue")
                },
                {
                    path: "shorts",
                    name: "shorts",
                    component: () => import("../pages/sub_pages/movie_lists/pages/ShortPage.vue")
                },
            ]
        },
        {
            path: "/youtube",
            name: "youtube_home",
            children: [
                {
                    path: '',
                    name: 'youtube',
                    component: () => import("../pages/sub_pages/youtube/YoutubePage.vue")
                },
                {
                    path: "yt_riot_games",
                    component: () => import("../pages/sub_pages/youtube/pages/YTRiotPage.vue")

                },
                {
                    path: "yt_animations",
                    component: () => import("../pages/sub_pages/youtube/pages/YTAnimationsPage.vue")
                },
                {
                    path: "yt_music_videos",
                    component: () => import("../pages/sub_pages/youtube/pages/YTMusicVideoPage.vue")
                },
                {
                    path: "yt_short_films",
                    component: () => import("../pages/sub_pages/youtube/pages/YTShortsPage.vue")
                },
                {
                    path: "yt_anime_openings",
                    component: () => import("../pages/sub_pages/youtube/pages/YTAnimeOpeningPage.vue")
                },
                {
                    path: "yt_overwatch_cinematics",
                    component: () => import("../pages/sub_pages/youtube/pages/YTOverwatchPage.vue")
                },
                {
                    path: "yt_comedy",
                    component: () => import("../pages/sub_pages/youtube/pages/YTComedyPage.vue")
                },
                {
                    path: "yt_documentaries",
                    component: () => import("../pages/sub_pages/youtube/pages/YTDocumentaryPage.vue")
                },
                {
                    path: "yt_essays",
                    component: () => import("../pages/sub_pages/youtube/pages/YTVideoEssayPage.vue")
                },
                {
                    path: "yt_shows",
                    component: () => import("../pages/sub_pages/youtube/pages/YTShowsPage.vue")
                },
                {
                    path: "yt_debug",
                    component: () => import("../pages/sub_pages/youtube/pages/YoutubeDebug.vue")
                },
            ],
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