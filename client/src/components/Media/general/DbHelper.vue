<script setup>
import {defineProps, defineEmits, ref, watch, onMounted, onUnmounted, computed, inject, provide} from 'vue'
import TagContainer from "@/components/Media/components/TagContainer";
import asset_paths from '../../../../public/assets/tags/assets.json'
import MovieContainer from "@/components/Media/MediaContainer";

const current_api = inject('curr_api')
const devMode = inject('devMode')
let forceVis = inject('forceVis')

const tag_path = "./assets/tags/icons/"

const props = defineProps(['data', 'open', 'mediaType'])
const emits = defineEmits(['opened', 'closed', 'updated'])

let MovChanges = ref({'title': 'test', 'my_rating': '0'})
let iconData = ref({
  'name': "",
  'description': "",
  'tier': "gold",
  'image': ""
})
const tempRange = ref({
  'avg_range': [0, 0],
  'my_range': [0, 1],
})

let tagPresets = ref({})

let currentSearchMovie = ref("")
let currentSearchType = ref(props['mediaType'])
let currentSearchPage = ref(0)
let extraPosters = ref([])
let currentPoster = ref(0)
let presentInDb = ref(false)

onMounted(() => {
  loadPresets()
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      closeHelper()
    }
    if (event.key === 'Enter') {
      updateMedia()
    }
  })
})

watch(props, (newV, oldV) => {
  MovChanges.value = newV.data

  if (newV.open === true) {
    forceVis.value = true
    getExtraPosters()
    checkInDb()
  }
})


const availableRegions = ["none", "western", "asian"]
const availableTiers = ["cyan", "gold", "green", "purple", "red", "silver"]
const availableReWatch = ["none", "up", "down"]


async function searchMovie() {
  const url = new URL(`${current_api}/media/search`)
  url.searchParams.set('type', currentSearchType.value)
  url.searchParams.set('title', currentSearchMovie.value)
  url.searchParams.set('page', String(currentSearchPage.value))

  fetch(url)

      // Handle http error
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        }
        return response.json()
      })

      // Process the returned JSON data
      .then(data => {
        MovChanges.value = data
        checkInDb()
        getExtraPosters()
        // if (devMode) console.log('searchMovie', data);
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

async function getExtraPosters() {
  const url = new URL(`${current_api}/media/extra_posters`)
  console.log('test',MovChanges.value)
  url.searchParams.set('media_id', MovChanges.value['imdb_id'] ? MovChanges.value['imdb_id'] : MovChanges.value['id'])
  url.searchParams.set('media_type', currentSearchType.value)

  fetch(url)

      // Handle http error
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        }
        return response.json()
      })

      // Process the returned JSON data
      .then(data => {
        extraPosters.value = data
        // if (devMode) console.log(data);
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

async function scrollPage(event) {
  currentSearchPage.value = Number(event.target.value)
  searchMovie()
}

async function addMovie(button) {
  button.target.disabled = true

  const url = new URL(`${current_api}/media/add`)
  const params = {
    'data': MovChanges.value,
    'media_type': currentSearchType.value
  }

  fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(params)
  })

      // Handle http error
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        } else {
          button.target.disabled = false
          closeHelper()
        }
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

async function delMovie(button) {
  button.target.disabled = true

  const url = new URL(`${current_api}/media/delete`)
  const params = {
    'data': MovChanges.value,
    'media_type': currentSearchType.value
  }

  fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(params)
  })

      // Handle http error
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        } else {
          button.target.disabled = false
          closeHelper()
          if (devMode) console.log('media deleted');
        }
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

async function updateMedia() {

  const url = new URL(`${current_api}/media/update`)
  const params = {
    'data': MovChanges.value,
    'media_type': currentSearchType.value
  }

  fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(params)
  })

      // Handle http error
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        }

        closeHelper()
        // if (devMode) console.log('media updated', MovChanges.value);
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

async function checkInDb() {
  const url = new URL(`${current_api}/media/check_dupe`)
  url.searchParams.set('media_type', currentSearchType.value)
  url.searchParams.set('media_id', MovChanges.value['id'])

  fetch(url)

      // Handle http error
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        }
        return response.json()
      })

      // Process the returned JSON data
      .then(data => {
        presentInDb.value = data['result'];
        // if (devMode) console.log(data);
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

async function changePoster(input) {

  // console.log('changing poster')
  if (input <= extraPosters.value.length) {
    currentPoster.value = input
    MovChanges.value['poster_path'] = extraPosters.value[currentPoster.value]
  }
}

async function addTagMovie() {
  if (MovChanges.value['tags'] === undefined) {
    MovChanges.value['tags'] = []
  }
  MovChanges.value['tags'].push({...iconData.value})
  // console.log('added tag', MovChanges.value)
}

async function delTagMovie() {
  MovChanges.value['tags'].forEach((tag, index) => {
    if (tag['name'] === iconData.value['name']) {
      MovChanges.value['tags'].splice(index, 1)
    }
  })
}

async function delAllTagMovie() {
  MovChanges.value['tags'] = []
}

async function loadPresets() {

  const url = new URL(`${current_api}/preset/get_all`)

  fetch(url)

      // Handle http error
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        }
        return response.json()
      })

      // Process the returned JSON data
      .then(data => {
        tagPresets.value = data
        // if (devMode) console.log(data);
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

async function addTagPresets() {

  const url = new URL(`${current_api}/preset/add`)
  const params = {'data': iconData.value}

  fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(params)
  })

      // Handle http error
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        }
        loadPresets()
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

async function delTagPresets() {

  const url = new URL(`${current_api}/preset/delete`)
  const params = {'data': iconData.value}

  fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(params)
  })

      // Handle http error
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        }
        loadPresets()
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

async function closeHelper() {
  forceVis.value = false
  emits('closed', true)
  emits('updated', true)
}

</script>
<template>
  <div v-if="open">
    <div class="background_blackout">...</div>
    <div class="main_win">

      <div v-if="MovChanges">
        <div class="poster_preview" v-if="extraPosters">
          <div class="poster_box" style="width: 150px"
               v-for="(poster,index) in extraPosters"
               :key="index">
            <img v-if="currentSearchType !== 'manga'" v-lazy="`https://image.tmdb.org/t/p/w500${poster}`" alt="poster"
                 @click="changePoster(index)" style="width: 150px;">
            <img v-if="currentSearchType === 'manga'"
                 v-lazy="`https://uploads.mangadex.org/covers/${poster}.256.jpg`" alt="poster"
                 @click="changePoster(index)" style="width: 150px;">
          </div>
        </div>
      </div>

      <div class="metadata_wrapper box_wrapper">

        <MovieContainer :data="MovChanges" :ratingRange="tempRange"
                        :media-type="currentSearchType" :force-hover="true"></MovieContainer>

        <div class="movie_adder box_wrapper input_tag_description">

          <label for="search_m_input">Search</label>
          <input type="search" @input="currentSearchMovie = $event.target.value" id="search_m_input">
          <button @click="searchMovie">Search</button>

          <label for="search_list_input">Search scroll</label>
          <input type="number" @change="scrollPage" value="0"
                 id="search_list_input">

        </div>

        <div class="metadata box_wrapper input_tag_description">
          <!--      Rating-->
          <label for="rating_input">Rating</label>
          <input type="number" id="rating_input" :value="MovChanges['my_rating']"
                 @change="MovChanges['my_rating'] = String($event.target.value)">

          <!--      Content rating-->
          <label for="content_rating">Content rating</label>
          <form id="content_rating" @click="MovChanges['contentRating'] = String($event.target.value)">
            <select>
              <option>safe</option>
              <option>suggestive</option>
              <option>erotica</option>
              <option>pornographic</option>
            </select>
          </form>
          <!--      Re-watch-->
          <div>
            <label for="re_watch">Re-watch</label>
            <form id="re_watch" @input="MovChanges['re_watch'] = String($event.target.value)">
              <select>
                <option v-for="elem in availableReWatch" :key="elem">{{ elem }}</option>
              </select>
            </form>
          </div>

          <div v-if="mediaType==='manga'">
            <label for="re_read">Re-read</label>
            <input id="re_read" type="number" @input="MovChanges['re_read'] = String($event.target.value)">

            <label for="dropped">Dropped</label>
            <input id="dropped" type="checkbox" @input="MovChanges['dropped'] = String($event.target.value)">
          </div>
          <!--          Date rated-->
          <label for="date_rated_input">Date rated</label>
          <input type="date" id="date_rated_input" :value="data['date_rated'] ? data['date_rated'] : null"
                 @change="MovChanges['date_rated'] = String($event.target.value)">
        </div>

        <div class="box_wrapper">
          <!--          <button @click="refreshData">Refresh data</button>-->
          <p v-if="presentInDb">!! Movie already added !!</p>
          <button @click="addMovie" v-if="!presentInDb">add movie</button>
          <button @click="delMovie">remove movie</button>
        </div>
      </div>

      <div class="icon_adder box_wrapper row_flow">
        <div class="box_wrapper">

          <div class="icon_settings box_wrapper">
            <div class="icon_metadata box_wrapper">
              <TagContainer :tag_input="[iconData]" :preview="true"></TagContainer>
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

          <div class="icon_selector box_wrapper" style="overflow-x: hidden">
            <div class="icon_selectable preset_icons" v-for="preset in tagPresets" :key="preset['name']"
                 @click="iconData={...preset}">
              <TagContainer :tag_input="[preset]" :preview="true"></TagContainer>
            </div>
          </div>

          <div class="box_wrapper">
            <button @click="addTagPresets">add to presets</button>
            <button @click="delTagPresets">remove from presets</button>
          </div>


        </div>

        <div class="icon_selector box_wrapper" style="min-height: 90vh; max-width: 20vw">
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

      <div class="upload box_wrapper" v-if="MovChanges">
        <button @click="closeHelper" style="width: 100%">Close</button>
        <button @click="updateMedia" v-if="MovChanges['my_rating']" style="width: 100%">upload changes</button>
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
  /*outline: 1px solid red;*/
  position: fixed;
  color: black;

  inset: 0;
  margin: auto;

  display: flex;
  flex-flow: column wrap;
  /*height: 800px;*/
  height: 90vh;
  width: 100%;
  z-index: 3000;
}

.background_blackout {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  /*outline: 1px solid red;*/
  z-index: 205;
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

.poster_preview {
  overflow: scroll;
  height: 90vh;
  width: 400px;
  /*background-color: white;*/
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  padding: 5px;

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
  max-height: 500px;
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