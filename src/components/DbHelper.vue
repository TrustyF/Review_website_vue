<script setup>
import {defineProps, defineEmits, ref, watch, onMounted, computed} from 'vue'
import asset_paths from '../../public/assets/tags/assets.json'
import axios from 'axios'
import TagContainer from "@/components/MovieContainer/TagContainer";
import MovieContainer from "@/components/MovieContainer/MovieContainer";

const props = defineProps(['data', 'open'])
let MovChanges = {}
const foundMovie = ref()

const apiKey = '063ccf740a391dee9759aaa3564661c2'

const editConfirmed = ref(false)

const iconTitle = ref("")
const iconDesc = ref("")
const iconImg = ref("")
const iconTier = ref("")

// const availableTypes = ["movie", "tv", "documentary"]
const availableRegions = ["western", "asian"]
const availableTiers = ["cyan", "gold", "green", "purple", "red", "silver"]

function addChange(target, change) {
  console.log(target, change)
  console.log(MovChanges)
  MovChanges[target] = change
}

function pushChange(button) {
  button.target.disabled = true
  // button.target.lastChild.data = " ❌"
  axios.post("http://localhost:5000/edit_movie/", {'newData': MovChanges, 'oldData': props.data})
      .then(response => {
        console.log("edit status", response.status)
        button.target.disabled = false
        // button.target.lastChild.data = " ✓"
      })
}

function searchMovie(query) {
  console.log('searching', query.target.value)
  axios.get(`https://api.themoviedb.org/3/search/movie?api_key=${apiKey}&language=en-US&query=${query.target.value}`)
      .then(response => {
        console.log("found movie", response.data['results'][0])
        foundMovie.value = response.data['results'][0]
      })

}

function addMovie(button) {
  button.target.disabled = true
  axios.post("http://localhost:5000/add_movie/", foundMovie.value)
      .then(response => {
        console.log("added movie")
        button.target.disabled = false
      })
}

</script>
<template>
  <div class="main_win">

    <div class="metadata box_wrapper">
      <p>{{ data.title }}</p>

      <!--      Rating-->
      <label for="rating_input">Rating</label>
      <input type="number" id="rating_input" :value="data['my_rating']"
             @change="addChange('my_rating',String($event.target.value))">
      <!--      Region-->
      <label for="region">Region</label>
      <form id="region" @change="addChange('region',String($event.target.value))">
        <select>
          <option v-for="elem in availableRegions" :key="elem" :selected="data['region']">{{ elem }}</option>
        </select>
      </form>

      <div class="upload box_wrapper">
        <button @click="pushChange($event)">upload changes</button>
      </div>

    </div>

    <div class="movie_adder box_wrapper">
      <label for="search_input">Search movie</label>
      <input @input="searchMovie">
      <!--      <p v-if="foundMovie">{{  foundMovie['poster_path'] }}</p>-->
      <img v-if="foundMovie" :src="`https://image.tmdb.org/t/p/w500${foundMovie['poster_path']}`" style="height: 150px"
           alt="poster">
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