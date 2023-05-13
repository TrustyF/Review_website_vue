<script setup>
import '../styles/globals.css'
import MovieContainer from "@/components/MovieContainer/MovieContainer";
import DbHelper from "@/components/DbHelper";
import FilterMenu from "@/components/Homepage/FilterMenu";
import RatingHeader from "@/components/Homepage/RatingHeader";
import {inject} from 'vue'

import axios from 'axios'
import {ref, onMounted} from 'vue'

// to do
// add fresh review
const current_api = inject('curr_api')
const devMode = inject('devMode')

const movies = ref([])

const excludeMode = ref(false)
const filters = ref({})

const currentSelectedMovie = ref({})
const currentSelectedRatings = ref([9, 8, 7, 6, 5, 4, 3, 2, 1])

let recentRatings = ref({})

const servStatus = ref(0)
let settingsOpen = ref(false)

onMounted(() => {
  get_recent_ratings()
})

function update_movies(input = {}) {
  // console.log('updating movies')
  axios.post(`${current_api}/get_movies/`, input)
      .then(response => {
        console.log("response", response)
        movies.value = response.data
        servStatus.value = response.status
      })
}

function get_recent_ratings() {
  axios.post(`${current_api}/get_recent_movie_ratings/`, {'window': window.innerWidth})
      .then(response => {
        console.log("response recent", response)
        recentRatings.value = response.data
      })
}

function editMovie(input) {
  settingsOpen.value = true
  currentSelectedMovie.value = input
}


</script>
<template>
  <db-helper v-if="devMode" :data="currentSelectedMovie" :open="settingsOpen"
             @closed="settingsOpen=!settingsOpen"></db-helper>

  <FilterMenu @filters="update_movies"></FilterMenu>

  <div class="feed" v-if="servStatus===200">

    <div class="movie_grid">
      <rating-header :rating="'Recent ratings'"></rating-header>
      <div class="movie_container_wrapper" v-for="rec in recentRatings" :key="rec.title + '_rec'">
        <MovieContainer :key="rec.id + '_rec'" :data="rec" @MovieEdit="editMovie"></MovieContainer>
      </div>
    </div>

    <div class="movie_grid" v-for="rating in [9,8,7,6,5,4,3,2,1]" :key="rating">
      <rating-header :rating="rating"></rating-header>
      <div class="movie_container_wrapper" v-for="mov in movies[`rank_${rating}`]" :key="mov.title">
        <MovieContainer :key="mov.id" :data="mov" @MovieEdit="editMovie"></MovieContainer>
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