<script setup>
import {defineProps, defineEmits, ref, watchEffect,watch, onMounted, computed, inject} from 'vue'
import asset_paths from '../../public/assets/tags/assets.json'
import axios from 'axios'
import TagContainer from "@/components/MovieContainer/TagContainer";
import MovieContainer from "@/components/MovieContainer/MovieContainer";

const props = defineProps(['data', 'open'])
let MovChanges = ref()

watch(props,(newV,oldV) => {
  console.log(newV)
  MovChanges.value = newV.data
})

const apiKey = '063ccf740a391dee9759aaa3564661c2'
const current_api = inject('curr_api')

const editConfirmed = ref(false)

const iconTitle = ref("")
const iconDesc = ref("")
const iconImg = ref("")
const iconTier = ref("")

// const availableTypes = ["movie", "tv", "documentary"]
const availableRegions = ["western", "asian"]
const availableTiers = ["cyan", "gold", "green", "purple", "red", "silver"]

function pushChange(button) {
  button.target.disabled = true
  // button.target.lastChild.data = " ❌"
  axios.post(`${current_api}/edit_movie/`, {'newData': MovChanges.value, 'oldData': props.data})
      .then(response => {
        console.log("edit status", response.status)
        button.target.disabled = false
        // button.target.lastChild.data = " ✓"
      })
}

function searchMovie(query,type="movie") {
  console.log('searching', query.target.value)
  axios.get(`https://api.themoviedb.org/3/search/${type}?api_key=${apiKey}&language=en-US&query=${query.target.value}`)
      .then(response => {
        console.log("found movie", response.data['results'][0])
        MovChanges.value = response.data['results'][0]
        console.log("curr movie", MovChanges)
      })

}

function addMovie(button) {
  button.target.disabled = true
  axios.post(`${current_api}/add_movie/`, MovChanges.value)
      .then(response => {
        console.log("added movie")
        button.target.disabled = false
      })
}

</script>
<template>
  <div class="main_win">

    <div class="metadata box_wrapper">

      <MovieContainer v-if="MovChanges" :data="MovChanges"></MovieContainer>

      <!--      Rating-->
      <label for="rating_input">Rating</label>
      <input type="number" id="rating_input" :value="data['my_rating']"
             @change="MovChanges['my_rating'] = String($event.target.value)">
      <!--      Region-->
      <label for="region">Region</label>
      <form id="region" @change="MovChanges['region'] = String($event.target.value)">
        <select>
          <option v-for="elem in availableRegions" :key="elem" :selected="data['region']">{{ elem }}</option>
        </select>
      </form>

      <div class="upload box_wrapper">
        <button @click="pushChange($event)">upload changes</button>
      </div>

    </div>

    <div class="movie_adder box_wrapper">

      <label for="search_m_input">Search movie</label>
      <input type="search" @submit="searchMovie($event,'movie')" id="search_m_input">

      <label for="search_t_input">Search tv</label>
      <input type="search" @keydown="searchMovie($event,'tv')" id="search_t_input">

      <button @click="addMovie">add movie</button>
    </div>


  </div>
</template>

<script>
export default {
  name: "DbHelper"
}
</script>

<style>
.main_win {
  display: flex;
  flex-flow: row;
}

.metadata {
  outline: 1px solid red;
}

.box_wrapper {
  /*width: 200px;*/
  display: flex;
  flex-flow: column;
  align-items: flex-start;
  gap: 5px;

  background-color: white;

  border: 1px solid black;
  border-radius: 5px;

  padding: 10px;
  margin: 5px;
}
</style>