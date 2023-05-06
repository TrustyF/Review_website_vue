<script setup>
import {defineProps, defineEmits, ref, watchEffect, watch, onMounted, computed, inject} from 'vue'
import TagContainer from "@/components/MovieContainer/components/TagContainer";
import asset_paths from '../../public/assets/tags/assets.json'

const tag_path = "./assets/tags/icons/"

import axios from 'axios'

const props = defineProps(['data', 'open'])
let MovChanges = ref()
let iconData = ref({
  'name':"",
  'description':"",
  'tier':"gold",
  'image':""
})

watch(iconData.value, (newV, oldV) => {
  console.log(iconData)
})

watch(props, (newV, oldV) => {
  console.log(newV)
  MovChanges.value = newV.data
})

const apiKey = '063ccf740a391dee9759aaa3564661c2'
const current_api = inject('curr_api')

const editConfirmed = ref(false)


// const availableTypes = ["movie", "tv", "documentary"]
const availableRegions = ["western", "asian"]
const availableTiers = ["cyan", "gold", "green", "purple", "red", "silver"]

let throttle_search = false

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

async function searchMovie(query, type = "movie") {
  let search_text = query.target.value

  if (throttle_search === true) return
  if (search_text.length < 1) return

  throttle_search = true
  console.log('searching', search_text)
  setTimeout(async function () {
    MovChanges.value = await axios.get(`https://api.themoviedb.org/3/search/${type}?api_key=${apiKey}&language=en-US&query=${search_text}`)
        .then(response => {

          if (response.data['results'].length < 1) {
            throttle_search = false
            return
          }

          const simple_data = response.data['results'][0]

          return axios.get(`https://api.themoviedb.org/3/${type}/${simple_data['id']}?api_key=${apiKey}&language=en-US&append_to_response=credits,images&include_image_language=en,null`)
              .then(response => {
                const full_data = response.data
                console.log('full_data', full_data)

                //replace genres
                simple_data['genres'] = full_data['genres'].map(a => a.name)
                delete simple_data['genre_ids']

                // add others
                simple_data['media_type'] = type
                simple_data['date_rated'] = new Date().toISOString().slice(0, 10)
                simple_data['extra_images'] = full_data['images']
                simple_data['runtime'] = full_data['runtime']

                // tv exceptions
                if (type === 'tv') {

                  simple_data['title'] = full_data['name']
                  delete simple_data['name']

                  simple_data['release_date'] = full_data['first_air_date']
                  delete simple_data['first_air_date']
                }

                console.log(simple_data)
                throttle_search = false
                return simple_data
              })
        })
  }, 300)
}

function addMovie(button) {
  button.target.disabled = true
  axios.post(`${current_api}/add_movie/`, MovChanges.value)
      .then(response => {
        console.log("added movie")
        button.target.disabled = false
      })
}

function delMovie(button) {
  button.target.disabled = true
  axios.post(`${current_api}/del_movie/`, MovChanges.value)
      .then(response => {
        console.log("removed movie")
        button.target.disabled = false
      })
}

function changePoster(input) {
  if (MovChanges.value['extra_images'] === undefined) return
  if (MovChanges.value['extra_images']['posters'] === undefined) return

  if (input.target.value <= MovChanges.value['extra_images']['posters'].length) {
    MovChanges.value['poster_path'] = MovChanges.value['extra_images']['posters'][input.target.value]['file_path']
  }
}

</script>
<template>
  <div class="main_win">

    <!--    <MovieContainer v-if="MovChanges" :data="MovChanges"></MovieContainer>-->

    <div class="metadata box_wrapper">
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

      <!--      Poster-->
      <label for="poster_input">Poster</label>
      <input type="number" id="poster_input" value="0"
             @change="changePoster">

      <div class="upload box_wrapper">
        <button @click="pushChange($event)">upload changes</button>
      </div>

    </div>

    <div class="movie_adder box_wrapper">

      <label for="search_m_input">Search movie</label>
      <input type="search" @input="searchMovie($event,'movie')" id="search_m_input">

      <label for="search_t_input">Search tv</label>
      <input type="search" @input="searchMovie($event,'tv')" id="search_t_input">

      <button @click="addMovie">add movie</button>
      <button @click="delMovie">remove movie</button>
    </div>

    <div class="icon_adder box_wrapper row_flow">
      <div class="icon_settings box_wrapper">
        <TagContainer :tag_input="[iconData]"></TagContainer>

        <input @change="iconData['name'] = String($event.target.value)">

        <form id="tier" @change="iconData['tier'] = String($event.target.value)">
          <select>
            <option v-for="tier in availableTiers" :key="tier">{{ tier }}</option>
          </select>
        </form>

      </div>
      <div class="icon_selector box_wrapper">
        <div class="icon_selectable" v-for="icon in asset_paths['icons'][iconData['tier']]" :key="icon"
             @click="iconData['image']=icon">
          <img v-lazy="`${tag_path}/${iconData['tier']}/${icon}`" style="width: 50px; height: 50px">
        </div>
      </div>
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
  max-height: 300px;
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

.row_flow {
  flex-flow: row;
}

.icon_adder {
  width: 1000px;
}

.icon_selector {
  display: flex;
  flex-flow: row wrap;
  overflow: scroll;
  height: 88%;
}

.icon_selectable {
  cursor: pointer;
  /*outline: 1px saddlebrown solid;*/
}
</style>