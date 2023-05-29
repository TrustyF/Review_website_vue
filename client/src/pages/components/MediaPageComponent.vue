<script setup>
import MovieContainer from "@/components/MediaContainer/Movies/MovieContainer";
import DbHelper from "@/components/DbHelper";
import RatingHeader from "@/components/Homepage/RatingHeader";
import {inject, watch, defineProps} from 'vue'

import axios from 'axios'
import {ref, onMounted, toRefs} from 'vue'
import FilterMenu from "@/components/Homepage/FilterMenu";

// to do
// add fresh review
const props = defineProps(['filters', 'ratingDesc', 'mediaType'])
const input_props = toRefs(props)

const current_api = inject('curr_api')
let devMode = inject('devMode')
let darkMode = inject('darkMode')
const sessionSeed = inject('sessionSeed')

const movies = ref([])
let filters = input_props['filters']
let ratingDesc = input_props['ratingDesc']
let mediaType = input_props['mediaType']
let settings = ref({
  'session_seed': sessionSeed,
})
const currentSelectedMovie = ref({})
const mediaRatingRanges = ref({})

const servStatus = ref(0)

// API

function setSettings() {
  console.log('set settings', `${current_api}/media/settings`)
  axios.post(`${current_api}/media/settings`, {
    'settings': settings.value,
    'media_type': mediaType.value,
    'filters': filters.value
  })
      .then(response => {
        console.log('set settings',response.status)
        getInfo()
      })
}

function getInfo() {
  axios.get(`${current_api}/media/info`)
      .then(response => {
        if (response.status === 200) {
          console.log('ranges',response.status)
          mediaRatingRanges.value = response.data['rating_range']
          update_movies()
        }
      })
}

function setFilters() {
  axios.post(`${current_api}/media/filters`, {
    'filters': filters.value
  })
      .then(response => {
        console.log('set filters',response.status)
        if (response.status === 200) {
          update_movies()
        }
      })
}

let fetchingMoreMovies = ref(false)

function fetchMoreMovies() {
  axios.get(`${current_api}/media/load_more`)
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
  axios.get(`${current_api}/media/all`)
      .then(response => {
        console.log('get movies',response.status)
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
  console.log('mounted', mediaType.value)
  setSettings()
  window.addEventListener('scroll', handleScroll)
})
</script>

<template>
  <div class="page">
    <db-helper v-if="devMode" :data="currentSelectedMovie" :open="settingsOpen" :mediaType="mediaType"
               @closed="settingsOpen = !settingsOpen" @updated="update_movies"></db-helper>
    <div v-if="devMode" style="visibility: hidden">
      <button @click="settingsOpen = true" style="margin: 13px 0 0 20px; position: fixed">Add {{ mediaType }}</button>
    </div>

    <FilterMenu :props="filters" @filtersChange="setFilters"></FilterMenu>

    <div class="feed" v-if="servStatus===200">

<!--      <div class="movie_grid">-->
<!--        <rating-header :rating="'Recent ratings'"></rating-header>-->
<!--        <div class="movie_container_wrapper" v-for="rec in recentRatings" :key="rec.title + '_rec'">-->
<!--          <MediaContainer :key="rec.id + '_rec'" :data="rec" @MovieEdit="editMovie"></MediaContainer>-->
<!--        </div>-->
<!--      </div>-->

      <div class="movie_grid" v-show="movies[rating].length > 0" v-for="rating in Object.keys(ratingDesc).reverse()" :key="rating">
        <rating-header  :rating="rating" :rating_desc="ratingDesc"></rating-header>
        <div class="movie_container_wrapper">
          <div v-for="mov in movies[rating]" :key="mov.title">
            <MovieContainer class="movie_container" :key="mov.id" :data="mov" :ratingRange="mediaRatingRanges"
                            @MovieEdit="editMovie"></MovieContainer>
          </div>
        </div>
      </div>

    </div>

    <div class="feed loader" v-else>
      Loading...
      <img :class="darkMode ? '': 'dark_image'" src="../../../public/assets/ui/Loading_icon.gif" alt="loading icon"
           style="width: 25px; margin: 10px">
    </div>
  </div>
</template>

<style scoped>

.page {
  transition: background-color 500ms;
}

.feed {
  /*outline: 1px solid blue;*/
  display: flex;
  flex-direction: column;
  margin: auto;
}

.loader {
  /*outline: 1px solid red;*/
  padding: 20px;
  display: flex;
  text-align: center;
  align-items: center;
}

.movie_grid {
  /*outline: 3px solid blue;*/
  margin: 30px;
  gap: 30px;
  display: flex;
  flex-flow: row wrap;
  justify-content: space-between;
}

.movie_container_wrapper {
  /*outline: 1px solid red;*/
  width: 80%;
  margin: auto;
  gap: 30px;

  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
}
</style>