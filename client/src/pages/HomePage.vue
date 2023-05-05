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

const movies = ref([])

const excludeMode = ref(false)
const filters = ref({})

const currentSelectedMovie = ref({})
const currentSelectedRatings = ref([9, 8, 7, 6, 5, 4, 3, 2, 1])

const servStatus = ref(0)
const settingsOpen = ref(false)

onMounted(() => {
  update_movies()
})

function update_movies(filters = {}) {
  // console.log('updating movies')
  axios.post(`${current_api}/get_movies/`, filters)
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

</script>
<template>
  <db-helper class="db_helper" :data="currentSelectedMovie" :open="settingsOpen"
             @settingsClosed="settingsOpen=!settingsOpen"></db-helper>

  <FilterMenu @filters="update_movies"></FilterMenu>

  <div class="feed" v-if="servStatus===200">
    <div class="movie_grid" v-for="rating in [9,8,7,6,5,4,3,2,1]" :key="rating">
      <rating-header :rating="rating"></rating-header>
      <div class="movie_container_wrapper" v-for="mov in movies[`rank_${rating}`]" :key="mov.title">
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

.db_helper {
  position: fixed;
  left: 0;
  bottom: 0;
  z-index: 20;
}
</style>