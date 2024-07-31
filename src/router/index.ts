import {createRouter, createWebHistory} from "vue-router";
import { getAnalytics, logEvent } from "firebase/analytics";

const media_types = ['movie', 'tv', 'short', 'youtube', 'anime', 'manga', 'game']

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
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
            path: "/short",
            name: "short",
            component: () => import("../pages/ShortPage.vue")
        },
        {
            path: "/youtube",
            name: "youtube",
            component: () => import("../pages/YoutubePage.vue")
        },
        {
            path: "/youtube/riot_games_media",
            name: "riot games media",
            component: () => import("../pages/sub_pages/youtube/YTRiotPage.vue")

        },
        {
            path: "/youtube/yt_animations",
            name: "youtube animations",
            component: () => import("../pages/sub_pages/youtube/YTAnimationsPage.vue")
        },
        {
            path: "/youtube/yt_music_videos",
            name: "youtube music videos",
            component: () => import("../pages/sub_pages/youtube/YTMusicVideoPage.vue")
        },
        {
            path: "/youtube/yt_short_films",
            name: "youtube short films",
            component: () => import("../pages/sub_pages/youtube/YTShortsPage.vue")
        },
        {
            path: "/youtube/yt_anime_openings",
            name: "youtube anime openings",
            component: () => import("../pages/sub_pages/youtube/YTAnimeOpeningPage.vue")
        },
        {
            path: "/youtube/yt_overwatch_cinematics",
            name: "youtube overwatch cinematics",
            component: () => import("../pages/sub_pages/youtube/YTOverwatchPage.vue")
        },
        {
            path: "/youtube/yt_comedy",
            name: "youtube comedy",
            component: () => import("../pages/sub_pages/youtube/YTComedyPage.vue")
        },
        {
            path: "/youtube/yt_documentaries",
            name: "youtube documentaries",
            component: () => import("../pages/sub_pages/youtube/YTDocumentaryPage.vue")
        },
        {
            path: "/youtube/yt_essays",
            name: "youtube essays",
            component: () => import("../pages/sub_pages/youtube/YTVideoEssayPage.vue")
        },
        {
            path: "/youtube/yt_shows",
            name: "youtube shows",
            component: () => import("../pages/sub_pages/youtube/YTShowsPage.vue")
        },
        {
            path: "/youtube/youtube_debug",
            name: "youtube debug",
            component: () => import("../pages/sub_pages/youtube/YoutubeDebug.vue")
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
            path: "/game",
            name: "game",
            component: () => import("../pages/GamePage.vue")
        },
        {
            path: "/debug_sql",
            name: "debug_sql",
            component: () => import("../pages/sub_pages/debug/test-sql.vue")
        },
    ],
})

router.beforeEach((to, from) => {
    setTimeout(()=>{
        window.scroll(0, 0)
    },1)

    const analytics = getAnalytics();
    logEvent(analytics, 'changed_page', {
        page_title: to.name,
    });
})
export default router