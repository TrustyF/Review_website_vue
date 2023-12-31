import {createRouter, createWebHistory} from "vue-router";

import HomePage from "../pages/HomePage.vue"
import MoviePage from "../pages/MoviePage.vue"
import MangaPage from "../pages/MangaPage.vue"
import SeriesPage from "../pages/SeriesPage.vue"
import ShortsPage from "../pages/ShortsPage.vue"
import AnimePage from "../pages/AnimePage.vue"
import GamePage from "../pages/GamePage.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomePage,
      // redirect: '/movie_picker'
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