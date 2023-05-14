<script setup>
import '../styles/globals.css'
import MovieContainer from "@/components/MovieContainer/MovieContainer";
import DbHelper from "@/components/DbHelper";
import FilterMenu from "@/components/Homepage/FilterMenu";
import RatingHeader from "@/components/Homepage/RatingHeader";
import {inject, watch} from 'vue'

import axios from 'axios'
import {ref, onMounted} from 'vue'

// to do
// add fresh review
const current_api = inject('curr_api')
const devMode = inject('devMode')
const sessionSeed = inject('sessionSeed')

const mangas = ref([])
let filters = ref({
  'type': {
    'name': 'Type',
    'available': ["Movie", "Tv-series", "Documentary"],
    'display': ["Movie", "Tv-series", "Documentary"],
    'filter': [],
    'checkbox': true,
  },
  'format': {
    'name': 'Format',
    'available': ["Live-action", "Animated"],
    'display': ["Filmed", "Animated"],
    'filter': [],
    'checkbox': false,
  },
  'region': {
    'name': 'Region',
    'available': ["western", "asian"],
    'display': ["Western", "Asian"],
    'filter': [],
    'checkbox': false,
  },
  'genre': {
    'name': 'Genre',
    'available': ["Action", "Adventure", "Crime", "Comedy", "Drama", "Family", "Horror", "Mystery", "Romance", "Science Fiction", "Thriller"],
    'display': ["Action", "Adventure", "Crime", "Comedy", "Drama", "Family", "Horror", "Mystery", "Romance", "Science Fiction", "Thriller"],
    'filter': [],
    'checkbox': true
  },
  'rating': {
    'name': 'Rating',
    'available': ["9", "8", "7", "6", "5", "4", "3", "2", "1"],
    'display': ["9★", "8★", "7★", "6★", "5★", "4★", "3★", "2★", "1★"],
    'filter': [],
    'checkbox': true
  },
  'length': {
    'name': 'Length',
    'available': ["0", "1", "2", "3"],
    'display': ["-1 hour", "1-2 hours", "2-3 hours", "3+ hours"],
    'filter': [],
    'checkbox': true
  },
  'sort': {
    'name': 'Sort',
    'available': ["0", "1"],
    'display': ["Popular vote", "Date rated"],
    'filter': [null],
  },
  'search_bar': "",
  'extra_settings': {
    'max_movies': 50,
    'session_seed': sessionSeed,
    're_watch':"",
    'media_type':"manga"
  }
})

const currentSelectedManga = ref({})
let recentRatings = ref({})

const servStatus = ref(0)
let settingsOpen = ref(false)
let scrollPosition = 0

onMounted(() => {
  // get_recent_ratings()
  update_manga()
})

watch(settingsOpen, (newV, oldV) => {
  settingsOpened()
})

function update_manga() {
  // console.log('updating mangas')
  axios.post(`${current_api}/get_movies/`, filters.value)
      .then(response => {
        // console.log("response", response)
        mangas.value = response.data
        servStatus.value = response.status
      })
}

function get_recent_ratings() {
  axios.post(`${current_api}/get_recent_movie_ratings/`, {'window': window.innerWidth})
      .then(response => {
        // console.log("response recent", response)
        recentRatings.value = response.data
      })
}

function editManga(input) {
  settingsOpen.value = true
  currentSelectedManga.value = input
}

function settingsOpened() {

  if (settingsOpen.value === false) {
    document.getElementsByClassName('feed')[0].style.position = 'relative'
    document.getElementsByClassName('feed')[0].style.overflowY = 'auto'
    window.scrollTo({top: scrollPosition, behavior: 'instant'})
  } else {
    scrollPosition = window.scrollY;
    document.getElementsByClassName('feed')[0].style.position = 'fixed'
    document.getElementsByClassName('feed')[0].style.overflowY = 'hidden'
  }
}

</script>
<template>
  <db-helper v-if="devMode" :data="currentSelectedManga" :mediaType="'manga'" :open="settingsOpen"
             @closed="settingsOpen = !settingsOpen"></db-helper>

  <FilterMenu :props="filters" @filtersChange="update_manga"></FilterMenu>

  <div v-if="devMode">
    <button @click="settingsOpen = true">Add manga</button>
  </div>

  <div class="feed" v-if="servStatus===200">

<!--    <div class="movie_grid">-->
<!--      <rating-header :rating="'Recent ratings'"></rating-header>-->
<!--      <div class="movie_container_wrapper" v-for="rec in recentRatings" :key="rec.title + '_rec'">-->
<!--        <MovieContainer :key="rec.id + '_rec'" :data="rec" @MovieEdit="editMovie"></MovieContainer>-->
<!--      </div>-->
<!--    </div>-->

    <div class="movie_grid" v-for="rating in [5,4,3,2,1]" :key="rating">
      <rating-header :rating="rating"></rating-header>
      <div class="movie_container_wrapper" v-for="manga in mangas[`rank_${rating}`]" :key="manga.title">
        <MovieContainer :key="manga.title" :data="manga" @MovieEdit="editManga"></MovieContainer>
      </div>
    </div>

  </div>

  <div class="feed loader" v-else>
    Loading...
    <img src="../../public/assets/ui/Loading_icon.gif" alt="loading icon" style="width: 25px; margin: 10px">
  </div>
</template>

<style scoped>
.feed {
  /*outline: 1px solid blue;*/
  position: relative;

  margin: 25px 15px 0 25px;

  display: flex;
  flex-direction: column;
}

.loader {
  /*outline: 1px solid red;*/
  display: flex;
  text-align: center;
  align-items: center;
  filter: brightness(0%);
}

.movie_grid {
  /*outline: 3px solid blue;*/
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  flex-flow: row wrap;
  margin: auto auto 20px;
}
</style>