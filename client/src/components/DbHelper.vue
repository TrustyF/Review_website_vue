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

let MovChanges = ref({'title': 'test', 'my_rating': '0'})
let iconData = ref({
  'name': "",
  'description': "",
  'tier': "gold",
  'image': ""
})

let tagPresets = ref({})

let currentSearchMovie = ref("")
let currentSearchType = ref("movie")
let currentSearchPage = ref(0)
let currentPoster = ref(0)
let presentInDb = ref(false)

loadPresets()

watch(props, (newV, oldV) => {
  MovChanges.value = newV.data
})

const availableRegions = ["western", "asian"]
const availableTiers = ["cyan", "gold", "green", "purple", "red", "silver"]
const availableReWatch = ["up", "down"]

let throttle_search = false

async function loadPresets() {
  tagPresets.value = await axios.get(`${current_api}/get_presets/`)
      .then(response => {
        // console.log(response.data)
        return response.data
      })
}

function pushChange(button) {
  button.target.disabled = true
  // button.target.lastChild.data = " ❌"
  axios.post(`${current_api}/edit_movie/`, {'newData': MovChanges.value, 'oldData': props.data})
      .then(response => {
        // console.log("edit status", response.status)
        button.target.disabled = false
        // button.target.lastChild.data = " ✓"
      })
  emits('closed',true)
}

async function searchMovie() {
  let search_text = currentSearchMovie.value

  console.log(search_text, currentSearchType.value, currentSearchPage.value)

  if (throttle_search === true) return
  if (search_text.length < 1) return

  throttle_search = true
  // console.log('searching', search_text)
  setTimeout(async function () {
    MovChanges.value = await axios.get(`https://api.themoviedb.org/3/search/${currentSearchType.value}?api_key=${apiKey}&language=en-US&query=${search_text}`)
        .then(response => {

          if (response.data['results'].length < 1) {
            throttle_search = false
            return
          }

          let simple_data = response.data['results'][currentSearchPage.value]

          return axios.get(`https://api.themoviedb.org/3/${currentSearchType.value}/${simple_data['id']}?api_key=${apiKey}&language=en-US&append_to_response=credits,images&include_image_language=en,null`)
              .then(response => {
                const full_data = response.data
                // console.log('full_data', full_data)

                //replace genres
                simple_data['genres'] = full_data['genres'].map(a => a.name)
                delete simple_data['genre_ids']

                // add others
                simple_data['media_type'] = currentSearchType.value
                // simple_data['date_rated'] = new Date().toISOString().slice(0, 10)
                simple_data['images'] = full_data['images']
                simple_data['runtime'] = full_data['runtime']

                // tv exceptions
                if (currentSearchType.value === 'tv') {

                  simple_data['title'] = full_data['name']
                  delete simple_data['name']

                  simple_data['release_date'] = full_data['first_air_date']
                  delete simple_data['first_air_date']
                }

                // console.log(simple_data)
                throttle_search = false
                return simple_data
              })
        })

    presentInDb.value = await axios.post(`${current_api}/check_dupe/`, {'text': MovChanges.value['title']})
        .then(response => {
          if (response.statusText === 'True') return true
          if (response.statusText === 'False') return false
        })
  }, 300)
}

function addMovie(button) {
  button.target.disabled = true
  axios.post(`${current_api}/add_movie/`, MovChanges.value)
      .then(response => {
        // console.log("added movie")
        button.target.disabled = false
      })
}

function delMovie(button) {
  button.target.disabled = true
  axios.post(`${current_api}/del_movie/`, MovChanges.value)
      .then(response => {
        // console.log("removed movie")
        button.target.disabled = false
      })
}

function changePoster(input) {
  if (MovChanges.value['images'] === undefined) return
  if (MovChanges.value['images']['posters'] === undefined) return

  // console.log('changing poster')
  if (input <= MovChanges.value['images']['posters'].length) {
    currentPoster.value = input
    MovChanges.value['poster_path'] = MovChanges.value['images']['posters'][currentPoster.value]['file_path']
  }
  console.log('posters', input, currentPoster.value)
}

function addTagMovie() {
  if (MovChanges.value['tags'] === undefined) {
    MovChanges.value['tags'] = []
  }
  MovChanges.value['tags'].push({...iconData.value})
  // console.log('added tag', MovChanges.value)
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
        // console.log("added preset")
        loadPresets()
      })
}

function delTagPresets() {
  axios.post(`${current_api}/del_preset/`, iconData.value)
      .then(response => {
        // console.log("removed preset")
        loadPresets()
      })
}

</script>
<template>
  <div v-if="open">
    <div class="background_blackout">...</div>
    <div class="main_win">

      <div class="poster_preview box_wrapper" v-if="MovChanges['images']"
           style="overflow: scroll; height:90vh; width: 10vw">
        <div class="poster_box" style="width: 9vw"
             v-for="(poster,index) in MovChanges['images']['posters']"
             :key="index">
          <img v-lazy="`https://image.tmdb.org/t/p/w500${poster['file_path']}`"
               @click="changePoster(index)" style="width: 100%;">
        </div>
      </div>

      <div class="metadata_wrapper box_wrapper">

        <MovieContainer class="preview_movie" v-if="MovChanges" :data="MovChanges"></MovieContainer>

        <div class="movie_adder box_wrapper">

          <label for="search_m_input">Search</label>
          <input type="search" @input="currentSearchMovie = $event.target.value" @change="searchMovie"
                 id="search_m_input">

          <label for="type">Type</label>
          <form id="type" @change="currentSearchType = String($event.target.value)">
            <select>
              <option v-for="elem in ['movie','tv']" :key="elem">{{ elem }}</option>
            </select>
          </form>

          <label for="search_list_input">Search scroll</label>
          <input type="number" @change="currentSearchPage = Number($event.target.value)" @input="searchMovie" value="0"
                 id="search_list_input">

        </div>

        <div class="metadata box_wrapper">
          <!--      Rating-->
          <label for="rating_input">Rating</label>
          <input type="number" id="rating_input"
                 @change="MovChanges['my_rating'] = String($event.target.value)">

          <!--      Region-->
          <label for="region">Region</label>
          <form id="region" @change="MovChanges['region'] = String($event.target.value)">
            <select>
              <option v-for="elem in availableRegions" :key="elem" :selected="data['region']">{{ elem }}</option>
            </select>
          </form>
          <!--      Re-watch-->
          <label for="region">Re-watch</label>
          <form id="region" @change="MovChanges['re_watch'] = String($event.target.value)">
            <select>
              <option v-for="elem in availableReWatch" :key="elem">{{ elem }}</option>
            </select>
          </form>
          <!--          Date rated-->
          <label for="date_rated_input">Date rated</label>
          <input type="date" id="date_rated_input" :value="data['date_rated']"
                 @change="MovChanges['date_rated'] = String($event.target.value)">

        </div>

        <div class="box_wrapper">
          <p v-if="presentInDb">!! Movie already added !!</p>
          <button @click="addMovie" v-if="!presentInDb">add movie</button>
          <button @click="delMovie">remove movie</button>
        </div>
      </div>

      <div class="icon_adder box_wrapper row_flow">
        <div class="box_wrapper">

          <div class="icon_settings box_wrapper">
            <div class="icon_metadata box_wrapper">
              <TagContainer :tag_input="[iconData]" :tooltip_override="false" style="min-height: 55px"></TagContainer>
            </div>

            <textarea @input="iconData['name'] = $event.target.value" :value="iconData['name']"
                      style="height: 15px"></textarea>
            <textarea class="input_tag_description" @input="iconData['description'] = $event.target.value"
                      :value="iconData['description']"></textarea>

            <div class="box_wrapper">
              <button @click="addTagMovie">add to movie</button>
              <button @click="delTagMovie">remove from movie</button>
              <button @click="delAllTagMovie">remove all from movie</button>
            </div>

          </div>

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

        <div class="icon_selector box_wrapper" style="min-height: 90vh; max-width: 30vw">
          <form id="tier" @input="iconData['tier'] = $event.target.value">
            <select>
              <option v-for="tier in availableTiers" :key="tier">{{ tier }}</option>
            </select>
          </form>

          <div class="icon_selectable" v-for="icon in asset_paths['icons'][iconData['tier']]" :key="icon"
               @click="iconData['image']=icon">
            <img v-lazy="`${tag_path}${iconData['tier']}/${icon}`" style="width: 50px; height: 50px">
          </div>
        </div>

      </div>

      <div class="upload box_wrapper">
        <button @click="pushChange($event)" v-if="MovChanges['my_rating']" style="width: 100%">upload changes</button>
        <button @click="emits('closed',true)" style="width: 100%">Close</button>
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
  outline: 1px solid red;
  position: fixed;

  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  margin: auto;

  display: flex;
  flex-flow: column wrap;
  /*height: 800px;*/
  height: 90vh;
  width: 85vw;
  z-index: 3000;
}

.background_blackout {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
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

.icon_selector {
  display: flex;
  flex-flow: row wrap;
  overflow: scroll;
  max-height: 90vh;
  max-width: 20vw;
}

.preset_icons {
  margin-right: -155px;
  margin-bottom: -5px;
}

.icon_selectable {
  cursor: pointer;
  /*outline: 1px saddlebrown solid;*/
}
</style>