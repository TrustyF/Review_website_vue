<template>
    <db-helper :open="settingsOpen" :input-data="currentSelectedMovie"></db-helper>

  <div class="filters">
    <h1 style="font-weight: bold; font-size: 1.5em">Filters</h1>
    <label class="filter_label">
      <input type="checkbox" style="cursor: pointer" @click="excludeMode = !excludeMode">
      Invert
    </label>

    <div class="filter_types" v-for="elem in filters" :key="elem['name']">
      <h1 style="text-decoration: underline;padding-bottom: 5px">{{ elem['name'] }}</h1>
      <div v-for="filter in elem['available']" :key="filter" class="filter_content_list">
        <label class="filter_label">
          <input type="checkbox" style="cursor: pointer" @change="swap_filter(filter,elem['filter']);update_movies()">
          {{ filter }}
        </label>
      </div>
    </div>

  </div>
  <div class="feed">
    <div class="movie_grid" v-for="rating in [9,8,7,6,5,4,3,2,1]" :key="rating">
      <div class="rating_container">
        <h1 class="rating_title">{{ rating }}</h1>
        <p class="rating_desc"> {{ getRankDetails(rating) }}</p>
      </div>
      <div class="movie_container_wrapper" v-for="mov in movies[`ranked_${rating}`]" :key="mov.id">
        <MovieContainer :key="mov.id" :data="mov" @debug_current_movie_data="debugSetCurrentMovie" @settings_open="settingsOpen = true"></MovieContainer>
      </div>

    </div>
  </div>
</template>

<script setup>
import '../styles/globals.css'
import MovieContainer from "@/components/MovieContainer";
import DbHelper from "@/components/DbHelper";

import axios from 'axios'
import {ref, onMounted} from 'vue'

// to do
// add addedDate, add fresh review, fix long titles


const movies = ref([])
const excludeMode = ref(false)
const currentSelectedMovie = ref({})
const settingsOpen = ref(false)
const filters = {
  'type': {
    'name': 'Type',
    'available': ["Movie", "Tv-series","Documentary"],
    'filter': [],
  },
  'format': {
    'name': 'Format',
    'available': ["Live-action", "Animated"],
    'filter': [],
  },
  'genre': {
    'name': 'Genre',
    'available': ["Action", "Adventure", "Crime", "Comedy", "Drama", "Family", "Horror", "Mystery", "Science Fiction", "Thriller"],
    'filter': [],
  },
  'rating': {
    'name': 'Rating',
    'available': ["9", "8", "7", "6", "5", "4", "3", "2", "1"],
    'filter': [],
  },
  'length': {
    'name': 'Length',
    'available': ["1", "2", "3"],
    'filter': [],
  },
}

const local_api = "http://localhost:5000"
const curr_api = "https://trustyfox.pythonanywhere.com"

onMounted(() => {
  update_movies()
})

function update_movies() {
  console.log('updating movies',filters)
  axios.post(`${local_api}/get_movies/`, filters)
      .then(response => {
        console.log(response.data)
        movies.value = response.data
      })
}

function swap_filter(filter, target) {
  console.log('swapping filter')
  if (target.includes(filter) === false) {
    target.push(filter)
  } else {
    let index = target.indexOf(filter)
    if (index > -1) { // only splice array when item is found
      target.splice(index, 1); // 2nd parameter means remove one item only
    }
  }
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

function debugSetCurrentMovie(input) {
  currentSelectedMovie.value = input
}


</script>

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

.filters {
  font-family: Calibri, serif;
  user-select: none;
  position: fixed;
  width: 150px;
  font-min-size: 1em;
  /*height: 200px;*/

  padding: 20px;
  margin: 15px 0 0 25px;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);

  display: flex;
  flex-flow: column;
  /*grid-template-areas:"left right";*/
  gap: 8px;
}

.filter_content_list {
  /*outline: red 1px solid;*/
  width: 100%;
}

.filter_label {
  font-size: 0.9em;
  cursor: pointer;
}
</style>