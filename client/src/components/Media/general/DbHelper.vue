<script setup>
import {defineProps, defineEmits, ref, watch, onMounted, onUnmounted, computed, inject} from 'vue'
import TagContainer from "@/components/Media/components/TagContainer";
import asset_paths from '../../../../public/assets/tags/assets.json'
import MovieContainer from "@/components/Media/MediaContainer";

const current_api = inject('curr_api')
const devMode = inject('devMode')

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
let currentPoster = ref(0)
let presentInDb = ref(false)

onMounted(() => {
  // loadPresets()
})

watch(props, (newV, oldV) => {
  MovChanges.value = newV.data
  checkInDb()
})

const availableRegions = ["none", "western", "asian"]
const availableTiers = ["cyan", "gold", "green", "purple", "red", "silver"]
const availableReWatch = ["none", "up", "down"]

async function loadPresets() {

  const url = new URL(`${current_api}/get_presets/`)
  url.searchParams.set('none', 'none')

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
        if (devMode) console.log(data);
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}


function searchMovie() {
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
        if (devMode) console.log('searchMovie', data);
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

function scrollPage(event) {
  currentSearchPage.value = Number(event.target.value)
  searchMovie()
}

// async function searchMovie() {
//   let search_text = currentSearchMovie.value
//   currentSearchPage.value = 0
//
//   console.log(search_text, currentSearchType.value, currentSearchPage.value)
//
//   if (throttle_search === true) return
//   if (search_text.length < 1) return
//
//   throttle_search = true
//   // console.log('searching', search_text)
//
//   if (currentSearchType.value === 'movie' || currentSearchType.value === 'tv') {
//     setTimeout(async function () {
//       let searchResult = await axios.get(`https://api.themoviedb.org/3/search/${currentSearchType.value}?api_key=${apiKey}&language=en-US&query=${search_text}`)
//           .then(response => {
//
//             if (response.data['results'].length < 1) {
//               throttle_search = false
//               return
//             }
//
//             let simple_data = response.data['results'][currentSearchPage.value]
//
//             return axios.get(`https://api.themoviedb.org/3/${currentSearchType.value}/${simple_data['id']}?api_key=${apiKey}&language=en-US&append_to_response=credits,images&include_image_language=en,null`)
//                 .then(response => {
//                   const full_data = response.data
//                   // console.log('full_data', full_data)
//
//                   //replace genres
//                   simple_data['genres'] = full_data['genres'].map(a => a.name)
//                   delete simple_data['genre_ids']
//
//                   // add others
//                   simple_data['media_type'] = currentSearchType.value
//                   // simple_data['date_rated'] = new Date().toISOString().slice(0, 10)
//                   simple_data['images'] = full_data['images']
//                   simple_data['runtime'] = full_data['runtime']
//
//                   // tv exceptions
//                   if (currentSearchType.value === 'tv') {
//
//                     simple_data['title'] = full_data['name']
//                     delete simple_data['name']
//
//                     simple_data['release_date'] = full_data['first_air_date']
//                     delete simple_data['first_air_date']
//                   }
//
// /*                  // console.log(simple_data)*/
// /*                  throttle_search = false*/
// /*                  return simple_data*/
//                 })
//           })
//
//       if (searchResult !== undefined) MovChanges.value = searchResult
//
//       await checkInDb()
//
//     }, 300)
//   }
//   if (currentSearchType.value === 'manga') {
//
//     setTimeout(async function () {
//           // console.log('searching manga')
//           let searchResult = await axios.get(`https://api.mangadex.org/manga?title=${search_text}&order%5Brelevance%5D=desc&includes[]=cover_art&limit=20`)
//               .then(response => {
//
// /*                // console.log('all found', response.data.data)*/
//
// /*                if (response.data.data.length < 1) {*/
// /*                  throttle_search = false*/
// /*                  return*/
// /*                }*/
//
// /*                if (response.data.data[currentSearchPage.value] === undefined) {*/
// /*                  throttle_search = false*/
// /*                  return*/
// /*                }*/
//
// /*                let simple_data = response.data.data[currentSearchPage.value]['attributes']*/
//                 let all_data = response.data.data[currentSearchPage.value]
//                 let formatted_data = {}
//                 console.log('simple_data', simple_data)
//                 // console.log('all_data', all_data)
//
//                 if (simple_data['title']['en'] !== undefined) formatted_data['title'] = simple_data['title']['en']
//                 if (simple_data['title']['en'] === undefined) formatted_data['title'] = simple_data['title']['ja']
//
//                 formatted_data['manga_id'] = all_data['id']
//                 formatted_data['contentRating'] = simple_data['contentRating']
//                 formatted_data['release_date'] = String(simple_data['year'] + '-01-01')
//                 formatted_data['overview'] = simple_data['description']['en']
//                 formatted_data['links'] = simple_data['links']
//                 formatted_data['media_type'] = 'manga'
//                 formatted_data['genres'] = []
//                 formatted_data['genres'] = simple_data['tags'].map((elem) => {
//                   if (elem['attributes']['group'] === 'genre') {
//                     return elem['attributes']['name']['en']
//                   }
//                 }).filter(Boolean)
//
//                 formatted_data['images'] = {'posters': []}
//
//                 console.log('returned formatted', formatted_data)
//                 throttle_search = false
//                 return formatted_data
//               })
//
//           if (searchResult !== undefined) MovChanges.value = searchResult
//
//           await axios.get(`https://api.mangadex.org/cover?limit=100&manga%5B%5D=${MovChanges.value['manga_id']}`)
//               .then(response => {
//                 // console.log('covers', response.data.data)
//                 MovChanges.value['images']['posters'] = response.data.data.map((elem) => {
//                   return {
//                     'file_path': `${MovChanges.value['manga_id']}/${elem['attributes']['fileName']}`,
//                     'volume': elem['attributes']['volume']
//                   }
//                 })
//                 MovChanges.value['images']['posters'].sort((a, b) => a.volume - b.volume)
//                 MovChanges.value['poster_path'] = MovChanges.value['images']['posters'][0]['file_path']
//               })
//
//           await axios.get(`https://api.mangadex.org/statistics/manga/${MovChanges.value['manga_id']}`)
//               .then(response => {
//                 // console.log('stats', response.data['statistics'][MovChanges.value['manga_id']])
//                 MovChanges.value['vote_average'] = response.data['statistics'][MovChanges.value['manga_id']]['rating']['average']
//               })
//
//           await checkInDb()
//         },
//         300
//     )
//   }
// }
// function checkInDb() {
//   return axios.post(`${current_api}/media/check_dupe/`, MovChanges.value)
//       .then(response => {
//         console.log('dupe check', response.statusText)
//         if (response.statusText === 'True') {
//           presentInDb.value = true
//         }
//         if (response.statusText === 'False') {
//           presentInDb.value = false
//         }
//       })
// }

// async function refreshData() {
//   if (currentSearchType.value === 'manga') {
//     let searchResult = await axios.get(`https://api.mangadex.org/manga?ids%5B%5D=${MovChanges.value['manga_id']}&order%5Brelevance%5D=desc&includes[]=cover_art&limit=20`)
//         .then(response => {
//           let simple_data = response.data.data[currentSearchPage.value]['attributes']
//           // console.log(simple_data['contentRating'],simple_data['year'])
//           MovChanges.value['contentRating'] = simple_data['contentRating']
//           MovChanges.value['release_date'] = String(simple_data['year'] + '-01-01')
//           updateMedia()
//         })
//   }
// }

function addMovie(button) {
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
        }
        return response.json()
      })

      // Process the returned JSON data
      .then(data => {
        button.target.disabled = false
        closeHelper()
        if (devMode) console.log(data);
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

function delMovie(button) {
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
        }

        button.target.disabled = false
        closeHelper()
        if (devMode) console.log('media deleted');
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

function updateMedia() {

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
        if (devMode) console.log('media updated');
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

function checkInDb() {
  console.log('checking in db', MovChanges.value['title'])
  const url = new URL(`${current_api}/media/check_dupe`)
  url.searchParams.set('media_type', currentSearchType.value)
  url.searchParams.set('media_id', MovChanges.value['id'])

  fetch(url)

      // Handle http error
      .then(response => {
        // presentInDb.value = response.json();
        console.log(response)
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
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

// function addTagPresets() {
//   axios.post(`${current_api}/add_preset/`, iconData.value)
//       .then(response => {
//         // console.log("added preset")
//         loadPresets()
//       })
// }

// function delTagPresets() {
//   axios.post(`${current_api}/del_preset/`, iconData.value)
//       .then(response => {
//         // console.log("removed preset")
//         loadPresets()
//       })
// }

function closeHelper() {
  emits('closed', true)
  emits('updated', true)
}

</script>
<template>
  <div v-if="open">
    <div class="background_blackout">...</div>
    <div class="main_win">

      <div v-if="MovChanges">
        <div class="poster_preview box_wrapper" v-if="MovChanges['images']"
             style="overflow: scroll; height:90vh; width: 10vw">
          <div class="poster_box" style="width: 9vw"
               v-for="(poster,index) in MovChanges['images']['posters']"
               :key="index">
            <img v-if="currentSearchType === 'movies'" v-lazy="`https://image.tmdb.org/t/p/w500${poster['file_path']}`"
                 @click="changePoster(index)" style="width: 100%;">
            <img v-if="currentSearchType === 'manga'"
                 v-lazy="`https://uploads.mangadex.org/covers/${poster['file_path']}.256.jpg`"
                 @click="changePoster(index)" style="width: 100%;">
          </div>
        </div>
      </div>

      <div class="metadata_wrapper box_wrapper">

        <MovieContainer :data="MovChanges" :ratingRange="tempRange"
                        :media-type="currentSearchType"></MovieContainer>

        <div class="movie_adder box_wrapper input_tag_description">

          <label for="search_m_input">Search</label>
          <input type="search" @input="currentSearchMovie = $event.target.value" @keyup.enter="searchMovie"
                 id="search_m_input">

          <label for="search_list_input">Search scroll</label>
          <input type="number" @change="scrollPage" value="0"
                 id="search_list_input">

        </div>

        <div class="metadata box_wrapper input_tag_description">
          <!--      Rating-->
          <label for="rating_input">Rating</label>
          <input type="number" id="rating_input"
                 @change="MovChanges['my_rating'] = String($event.target.value)">

          <!--      Region-->
          <label for="region">Region</label>
          <form id="region" @click="MovChanges['region'] = String($event.target.value)">
            <select>
              <option v-for="elem in availableRegions" :key="elem" :selected="data['region']">{{ elem }}</option>
            </select>
          </form>
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

      <div class="upload box_wrapper" v-if="MovChanges">
        <button @click="updateMedia($event)" v-if="MovChanges['my_rating']" style="width: 100%">upload changes</button>
        <button @click="closeHelper" style="width: 100%">Close</button>
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
  width: 85vw;
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