<script setup>
import {defineProps, defineEmits, ref, watch, onMounted, computed, inject} from 'vue'
import TagContainer from "@/components/MovieContainer/components/TagContainer";
import asset_paths from '../../public/assets/tags/assets.json'
import MovieContainer from "@/components/MovieContainer/MovieContainer";

const apiKey = '063ccf740a391dee9759aaa3564661c2'
const current_api = inject('curr_api')

const tag_path = "./assets/tags/icons/"

import axios from 'axios'

const props = defineProps(['data', 'open'])
const emits = defineEmits(['closed'])

let MovChanges = ref({'title': 'test'})
let iconData = ref({
  'name': "",
  'description': "",
  'tier': "gold",
  'image': ""
})
let tagPresets = ref({})
loadPresets()

watch(props, (newV, oldV) => {
  console.log('prop change', newV)
  MovChanges.value = newV.data
})

watch(iconData.value, (newV, oldV) => {
  console.log('icon change', newV)
})

async function loadPresets() {
  tagPresets.value = await axios.get(`${current_api}/get_presets/`)
      .then(response => {
        console.log(response.data)
        return response.data
      })
}

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
                simple_data['images'] = full_data['images']
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
  console.log('posters',MovChanges.value)
  if (MovChanges.value['images'] === undefined) return
  if (MovChanges.value['images']['posters'] === undefined) return

  console.log('changing poster')
  if (input.target.value <= MovChanges.value['images']['posters'].length) {
    MovChanges.value['poster_path'] = MovChanges.value['images']['posters'][input.target.value]['file_path']
  }
}

function addTagMovie() {
  if (MovChanges.value['tags'] === undefined) {
    MovChanges.value['tags'] = []
  }
  MovChanges.value['tags'].push({...iconData.value})
  console.log('added tag', MovChanges.value)
}

function delTagMovie() {
  MovChanges.value['tags'].forEach((tag, index) => {
    if (tag['name'] === iconData.value['name']) {
      MovChanges.value['tags'].splice(index, 1)
    }
  })
}

function delAllTagMovie() {
  MovChanges.value['tags'] = []
}

function addTagPresets() {
  axios.post(`${current_api}/add_preset/`, iconData.value)
      .then(response => {
        console.log("added preset")
        loadPresets()
      })
}

function delTagPresets() {
  axios.post(`${current_api}/del_preset/`, iconData.value)
      .then(response => {
        console.log("removed preset")
        loadPresets()
      })
}

</script>
<template>
  <div v-if="open">
    <div class="background_blackout">...</div>
    <div class="main_win">

      <MovieContainer class="preview_movie" v-if="MovChanges" :data="MovChanges"></MovieContainer>

      <div class="movie_adder box_wrapper">

        <label for="search_m_input">Search movie</label>
        <input type="search" @input="searchMovie($event,'movie')" id="search_m_input">

        <label for="search_t_input">Search tv</label>
        <input type="search" @input="searchMovie($event,'tv')" id="search_t_input">

      </div>

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


      </div>

      <div class="box_wrapper">
        <button @click="addMovie">add movie</button>
        <button @click="delMovie">remove movie</button>
      </div>

      <div class="icon_adder box_wrapper row_flow">
        <div class="icon_settings box_wrapper">
          <div class="icon_metadata box_wrapper">
            <TagContainer :tag_input="[iconData]" :tooltip_override="false"></TagContainer>
          </div>

          <textarea @input="iconData['name'] = $event.target.value" :value="iconData['name']" style="height: 15px"></textarea>
          <textarea class="input_tag_description" @input="iconData['description'] = $event.target.value" :value="iconData['description']"></textarea>

          <div class="box_wrapper">
            <button @click="addTagMovie">add to movie</button>
            <button @click="delTagMovie">remove from movie</button>
            <button @click="delAllTagMovie">remove all from movie</button>
          </div>

        </div>

        <div class="box_wrapper" style="height: 800px">
        <div class="icon_selector box_wrapper">
          <div class="icon_selectable preset_icons" v-for="preset in tagPresets" :key="preset['name']"
               @click="iconData={...preset}">
            <TagContainer :tag_input="[preset]"></TagContainer>
          </div>
        </div>

        <div class="box_wrapper">
          <button @click="addTagPresets">add to presets</button>
          <button @click="delTagPresets">remove from presets</button>
        </div>

        </div>

        <form id="tier" @input="iconData['tier'] = $event.target.value">
          <select>
            <option v-for="tier in availableTiers" :key="tier">{{ tier }}</option>
          </select>
        </form>

        <div class="icon_selector box_wrapper">
          <div class="icon_selectable" v-for="icon in asset_paths['icons'][iconData['tier']]" :key="icon"
               @click="iconData['image']=icon">
            <img v-lazy="`${tag_path}${iconData['tier']}/${icon}`" style="width: 50px; height: 50px">
          </div>
        </div>

      </div>

      <div class="upload box_wrapper">
        <button @click="pushChange($event)">upload changes</button>
        <button @click="emits('closed',true)">Close</button>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "DbHelper"
}
</script>

<style scoped>
.main_win {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-60%, -50%);
  display: flex;
  flex-flow: column wrap;
  height: 800px;
  z-index: 30;
}

.background_blackout {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 300%;
  /*outline: 1px solid red;*/
  z-index: 25;
  background-color: rgba(0, 0, 0, 75%);
}

.box_wrapper {
  /*outline: 1px solid red;*/
  /*min-width: 100px;*/
  display: flex;
  flex-flow: column;
  align-items: flex-start;
  gap: 5px;

  background-color: white;

  border: 1px solid black;
  border-radius: 5px;

  padding: 5px;
}

.row_flow {
  flex-flow: row;
}
.input_tag_description {
  width: 200px;
  font-family: inherit;
  font-weight: lighter;
  font-size: 0.7em;
}

.icon_adder {
  /*width: 500px;*/
}

.icon_selector {
  display: flex;
  flex-flow: row wrap;
  overflow: scroll;
  max-height: 800px;
  min-width: 500px;
}

.preset_icons {
  margin-right: -150px;
}

.icon_selectable {
  cursor: pointer;
  /*outline: 1px saddlebrown solid;*/
}
</style>