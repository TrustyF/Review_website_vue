<script setup>
import '../styles/globals.css'
import MovieContainer from "@/components/MovieContainer/MovieContainer";
import DbHelper from "@/components/DbHelper";
import FilterMenu from "@/components/Homepage/FilterMenu";
import RatingHeader from "@/components/Homepage/RatingHeader";

import axios from 'axios'
import {ref, onMounted} from 'vue'

// to do
// add fresh review, fix long titles

const movies = ref([])

const excludeMode = ref(false)
const filters = ref({})

const currentSelectedMovie = ref({})
const currentSelectedRatings = ref([9,8,7,6,5,4,3,2,1])

const servStatus = ref(0)
const settingsOpen = ref(false)

const local_api = "http://localhost:5000"
const curr_api = "https://trustyfox.pythonanywhere.com"

onMounted(() => {
  update_movies()
})

function update_movies() {
  // console.log('updating movies')
  axios.post(`${local_api}/get_movies/`, filters.value)
      .then(response => {
        // console.log("response",response)
        movies.value = response.data
        servStatus.value = response.status
      })
}

function closeSettings(input) {
  settingsOpen.value = input
}

function editMovie(input) {
  settingsOpen.value = true
  currentSelectedMovie.value = input
  console.log('emit caught')
}

function reactFilters(input) {
  // console.log('reacting to filter change', input)
  filters.value = input

  // currentSelectedRatings.value = input['rating']['filter']

  update_movies()
}

</script>
<template>
  <db-helper :data="currentSelectedMovie" :open="settingsOpen" @settingsClosed="closeSettings"></db-helper>

  <FilterMenu @filters="reactFilters"></FilterMenu>

  <div class="feed" v-if="servStatus===200">
    <div class="movie_grid" v-for="rating in currentSelectedRatings" :key="rating">
    <rating-header :rating="rating"></rating-header>
      <div class="movie_container_wrapper" v-for="mov in movies[`ranked_${rating}`]" :key="mov.id">
        <MovieContainer :key="mov.id" :data="mov" @MovieEdit="editMovie"></MovieContainer>
      </div>
    </div>
  </div>
  <div class="feed" v-else>Loading...</div>
</template>

<style scoped>
.feed {
  /*outline: 1px solid blue;*/
  position: relative;

  margin: 25px 15px 0 25px;

  display: flex;
  flex-direction: column;
}

.movie_grid {
  /*outline: 3px solid blue;*/
  width: 100%;

  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  flex-flow: row wrap;
  margin: auto;
}
</style>