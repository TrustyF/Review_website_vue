<script setup>
import MovieContainer from "@/components/Media/MediaContainer";
import DbHelper from "@/components/Media/general/DbHelper";
import RatingHeader from "@/components/Media/general/RatingHeader";
import {inject, watch, defineProps} from 'vue'

import {ref, onMounted, toRefs} from 'vue'
import FilterMenu from "@/components/Media/general/FilterMenu";
import {eventThrottle} from "@/utils";

// to do
// add fresh review
const props = defineProps(['filters', 'ratingDesc', 'mediaType'])
const input_props = toRefs(props)

const current_api = inject('curr_api')
let devMode = inject('devMode')
const mediaRanges = inject('mediaRanges')
const sessionSeed = inject('sessionSeed')

const movies = ref([])
const moviesFetched = ref(false)
let filters = input_props['filters']
let ratingDesc = input_props['ratingDesc']
let mediaType = input_props['mediaType']
let settings = ref({
  'session_seed': sessionSeed,
})

let maxMedia = ref(50)

const currentSelectedMovie = ref({})
const mediaRatingRanges = ref({})

// API
function update_movies() {

  const url = new URL(`${current_api}/media/get_all`)
  const params = {
    'settings': settings.value,
    'media_type': mediaType.value,
    'filters': filters.value,
    'max_media': maxMedia.value,
  }

  fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(params)
  })

      // Handle http error
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        }
        return response.json()
      })

      // Process the returned JSON data
      .then(data => {
        movies.value = data
        moviesFetched.value = true
        if (devMode) console.log('get movies', data);
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
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

  if (scrollTop + clientHeight >= (scrollHeight - (scrollHeight / 3))) {
    maxMedia.value += 50
    update_movies()
  }
}

watch(settingsOpen, (newV, oldV) => {
  settingsOpened()
})

onMounted(() => {
  update_movies()
  window.addEventListener('scroll', eventThrottle(handleScroll, 300))
})
</script>

<template>
  <div class="page">
    <db-helper v-if="devMode" :data="currentSelectedMovie" :open="settingsOpen" :mediaType="mediaType"
               @closed="settingsOpen = !settingsOpen" @updated="update_movies"></db-helper>
    <div v-if="devMode" style="visibility: hidden">
      <button @click="settingsOpen = true" style="margin: 13px 0 0 20px; position: fixed">Add {{ mediaType }}</button>
    </div>

    <FilterMenu :props="filters" @filtersChange="update_movies"></FilterMenu>

    <div class="feed" v-if="moviesFetched">

      <div class="movie_grid" v-show="movies[rating].length > 0" v-for="rating in Object.keys(ratingDesc).reverse()"
           :key="rating">
        <rating-header :rating="rating" :rating_desc="ratingDesc"></rating-header>
        <div class="movie_container_wrapper">
          <div v-for="mov in movies[rating]" :key="mov.title">
            <MovieContainer class="movie_container"
                            :key="mov.id"
                            :data="mov"
                            :ratingRange="mediaRanges[mediaType]"
                            :media-type="mediaType"
                            @MovieEdit="editMovie"></MovieContainer>
          </div>
        </div>
      </div>

    </div>

    <div class="feed loader" v-else>
      Loading...
      <img src="../../../public/assets/ui/Loading_icon.gif" alt="loading icon"
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