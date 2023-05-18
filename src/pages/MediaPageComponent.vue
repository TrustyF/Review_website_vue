<script setup>
import '../styles/globals.css'
import MovieContainer from "@/components/MediaContainer/Movies/MovieContainer";
import MangaContainer from "@/components/MediaContainer/Manga/MangaContainer";
import DbHelper from "@/components/DbHelper";
import FilterMenu from "@/components/Homepage/FilterMenu";
import RatingHeader from "@/components/Homepage/RatingHeader";
import {inject, watch, defineProps} from 'vue'

import axios from 'axios'
import {ref, onMounted,toRefs} from 'vue'

// to do
// add fresh review
const props = defineProps(['filters','ratingDesc','mediaType'])
const input_props = toRefs(props)

const current_api = inject('curr_api')
const devMode = inject('devMode')
const sessionSeed = inject('sessionSeed')

const movies = ref([])
let filters = input_props['filters']
let ratingDesc = input_props['ratingDesc']
let mediaType = input_props['mediaType']
let settings = ref({
  'session_seed': sessionSeed,
})
const currentSelectedMovie = ref({})

const servStatus = ref(0)

// API
function setMediaType(type) {
  axios.post(`${current_api}/set_media_type`, {'media_type': type})
      .then(() => setSettings())
}

function setSettings() {
  axios.post(`${current_api}/set_settings`, settings.value)
      .then(() => update_movies())
}

function setFilters() {
  axios.post(`${current_api}/set_filters`, filters.value)
      .then(response => {
        if (response.status === 200) {
          update_movies()
        }
      })
}

let fetchingMoreMovies = ref(false)

function fetchMoreMovies() {
  axios.post(`${current_api}/load_more`)
      .then(response => {
        console.log(response.status)
        if (response.status === 200) {
          fetchingMoreMovies.value = false
          update_movies()
        }
        if (response.status === 201) {
          console.log('max movies reached')
          update_movies()
        }
      })
}

function update_movies() {
  // console.log('updating movies')
  axios.get(`${current_api}/get_media`)
      .then(response => {
        console.log("response", response)
        movies.value = response.data
        servStatus.value = response.status
      })
}

function editMovie(input) {
  settingsOpen.value = true
  currentSelectedMovie.value = input
}

// Page helpers
let settingsOpen = ref(false)
let scrollPosition = 0

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

function handleScroll() {
  const scrollTop = document.documentElement.scrollTop
  const scrollHeight = document.documentElement.scrollHeight
  const clientHeight = document.documentElement.clientHeight

  if (scrollTop + clientHeight >= (scrollHeight - (scrollHeight / 3)) && fetchingMoreMovies.value === false) {
    fetchingMoreMovies.value = true
    setTimeout(function () {
      fetchMoreMovies()
    }, 300)
  }
}

watch(settingsOpen, (newV, oldV) => {
  settingsOpened()
})

onMounted(() => {
  console.log('mounted',mediaType)
  setMediaType(input_props['mediaType'].value)
  window.addEventListener('scroll', handleScroll)
})
</script>

<template>
  <db-helper v-if="devMode" :data="currentSelectedMovie" :open="settingsOpen" :mediaType="mediaType"
             @closed="settingsOpen = !settingsOpen"></db-helper>

  <FilterMenu :props="filters" @filtersChange="setFilters"></FilterMenu>

  <div v-if="devMode">
    <button @click="settingsOpen = true">Add {{mediaType}}</button>
  </div>

  <div class="feed" v-if="servStatus===200">

    <!--    <div class="movie_grid">-->
    <!--      <rating-header :rating="'Recent ratings'"></rating-header>-->
    <!--      <div class="movie_container_wrapper" v-for="rec in recentRatings" :key="rec.title + '_rec'">-->
    <!--        <MediaContainer :key="rec.id + '_rec'" :data="rec" @MovieEdit="editMovie"></MediaContainer>-->
    <!--      </div>-->
    <!--    </div>-->

    <div class="movie_grid" v-for="rating in Object.keys(ratingDesc).reverse()" :key="rating">
      <rating-header :rating="rating" :rating_desc="ratingDesc"></rating-header>
      <div class="movie_container_wrapper" v-for="mov in movies[rating]" :key="mov.title">
        <MovieContainer v-if="mediaType==='movie'" :key="mov.id" :data="mov" @MovieEdit="editMovie"></MovieContainer>
        <MangaContainer v-if="mediaType==='manga'" :key="mov.id" :data="mov" @MovieEdit="editMovie"></MangaContainer>
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