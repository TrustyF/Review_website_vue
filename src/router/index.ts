import {createRouter, createWebHistory} from "vue-router";

import MoviePage from "../pages/MoviePage.vue"
import MangaPage from "../pages/MangaPage.vue"
import SeriesPage from "../pages/SeriesPage.vue"
import AnimePage from "../pages/AnimePage.vue"
import GamePage from "../pages/GamePage.vue"
import MoviePickerPage from "../pages/MoviePickerPage.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
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