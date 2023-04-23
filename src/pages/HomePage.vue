<script setup>
import '../styles/globals.css'
import MovieContainer from "@/components/MovieContainer";
import DbHelper from "@/components/DbHelper";
import HomeFilter from "@/components/Homepage/HomeFilter";

import axios from 'axios'
import {ref, onMounted} from 'vue'

// to do
// add addedDate, add fresh review, fix long titles

const movies = ref([])

const excludeMode = ref(false)
const filters = ref({})

const currentSelectedMovie = ref({})

const servStatus = ref(0)
const settingsOpen = ref(false)

const local_api = "http://localhost:5000"
const curr_api = "https://trustyfox.pythonanywhere.com"

onMounted(() => {
  update_movies()
})

function update_movies() {
  console.log('updating movies')
  axios.post(`${local_api}/get_movies/`, filters.value)
      .then(response => {
        console.log(response)
        movies.value = response.data
        servStatus.value = response.status
      })
}

function getRankDetails(rank) {
  if (rank === 10) return 'Perfect'
  if (rank === 9) return 'Near perfect masterpiece'
  if (rank === 8) return 'Extremely good'
  if (rank === 7) return 'Quite good'
  if (rank === 6) return 'Good with flaws'
  if (rank === 5) return "Meh"
  if (rank === 4) return 'Bad'
  if (rank === 3) return 'Fucking bad'
  if (rank === 2) return 'Holy shit bad'
  if (rank === 1) return 'Affront to god'
}
function closeSettings(input){
  settingsOpen.value = input
}

function reactCurrentMovie(input) {
  settingsOpen.value = true
  currentSelectedMovie.value = input
}
function reactFilters(input){
  console.log('reacting to filter change',input)
  filters.value = input
  update_movies()
}

</script>
<template>
  <db-helper :inputData="currentSelectedMovie" :isOpen="settingsOpen" @settingsClosed="closeSettings"></db-helper>

  <HomeFilter @filters="reactFilters"></HomeFilter>

  <div class="feed" v-if="servStatus===200">

    <div class="movie_grid" v-for="rating in [9,8,7,6,5,4,3,2,1]" :key="rating">
      <div class="rating_container">
        <h1 class="rating_title">{{ rating }}</h1>
        <p class="rating_desc"> {{ getRankDetails(rating) }}</p>
      </div>

      <div class="movie_container_wrapper" v-for="mov in movies[`ranked_${rating}`]" :key="mov.id">

        <MovieContainer :key="mov.id" :data="mov" @debug_current_movie_data="reactCurrentMovie"></MovieContainer>

      </div>

    </div>
  </div>
  <div class="feed" v-else>Loading...</div>
</template>

<style scoped>
.feed {
  /*outline: 1px solid blue;*/

  position: relative;


  margin-left: 250px;
  margin-right: 20px;

  display: flex;
  flex-direction: column;
}

.rating_container {
  width: 100%;
  user-select: none;
}

.rating_title {
  font-family: "Arial Black", serif;
  padding: 10px 5px 5px 0;
  font-size: 2em;
  border-bottom: solid black 1px;
}

.rating_desc {
  /*font-family: Calibri;*/
  font-size: 1em;
  position: absolute;
  transform: translate(35px, -25px);
}

.movie_grid {
  /*outline: 1px solid red;*/

  width: 100%;

  display: flex;
  flex-wrap: wrap;
  /*justify-content: space-between;*/
  flex-flow: row wrap;
  margin: auto;
}


</style>