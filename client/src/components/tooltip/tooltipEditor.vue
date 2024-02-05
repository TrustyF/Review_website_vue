<script setup>
import {inject, onMounted, watch, ref, computed, onUnmounted, toRef} from "vue";
import FilterSearch from "@/components/media_filters/filterSearch.vue";
import MovieContainer from "@/components/media_container/movie_container/MovieContainer.vue";
import TagPicker from "@/components/editor_tools/TagPicker.vue";
import TierListPicker from "@/components/editor_tools/TierListPicker.vue";
import {get_current_user} from "@/firebase_auth.js";

let props = defineProps(["edit", "add"]);
// let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");
let selected_media = inject('selected_media')

let edit_pane_open = inject('edit_pane_open')
let add_pane_open = inject('add_pane_open')

let search_type = ref('movie')

let search_media = ref()
let search_text = ref('')
let search_page = ref(0)
let extra_posters = ref([])

let updated = ref('none')
let added = ref('none')
let hard_delete_count = ref(0)

let content_ratings = ref()
let all_content_ratings = ref()

let container_size = computed(() => {
  if (search_type.value === 'youtube') {
    return [1280 / 1.3, 720 / 1.3]
  } else {
    return [500, 750]
  }
})

async function fetch_filters() {

  const url = new URL(`${curr_api}/media/get_filters`)
  const params = {
    'type': selected_media.value['media_type'],
    'tier_lists': [],
  }

  const result = await fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(params)
  }).then(response => response.json())

  content_ratings.value = result['content_ratings']
  all_content_ratings.value = result['all_content_ratings']
  // content_ratings.value.push({'id': 0, 'name': 'None', 'order': -1})
  content_ratings.value.sort((a, b) => a['order'] > b['order'])
  all_content_ratings.value.sort((a, b) => a['order'] > b['order'])

  console.log('content ratings', content_ratings.value)
  // console.log(selected_media.value.content_rating)
}

async function get_media() {

  const url = new URL(`${curr_api}/media/get`)
  const params = {
    'type': search_type.value,
    'limit': 5,
    'page': 0,
    'session_seed': 1,
    'search': search_text.value,
    'order': 'date_added',
    'user_rating_sort_override': true,
    'random_sort_override': true,
  }

  search_media.value = await fetch(url,
      {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(params)
      })
      .then(response => response.json())
  updated.value = 'none'
  added.value = 'none'

}

async function find_media() {
  const token = await get_current_user()

  const url = new URL(`${curr_api}/media/find`)
  url.searchParams.set('name', search_text.value)
  url.searchParams.set('type', search_type.value)
  url.searchParams.set('page', String(search_page.value))

  search_media.value = await fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': token.uid,
      'Content-Type': 'application/json',
    }
  }).then(response => response.json())
  console.log(search_media.value)
  updated.value = 'none'
  added.value = 'none'
}

async function update_media() {
  const token = await get_current_user()

  if (selected_media.value['id'] === undefined) return

  console.log('updating', selected_media.value)

  const url = new URL(`${curr_api}/media/update`)

  const result = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': token.uid,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(selected_media.value)
  }).then(response => response.json())

  updated.value = result.ok ? 'true' : 'false'
  setTimeout(()=>updated.value = 'none',3000)

  if (updated.value) handle_pane_close()
}

async function hard_delete() {
  const token = await get_current_user()

  if (selected_media.value['id'] === undefined) return
  if (hard_delete_count.value < 2) {
    hard_delete_count.value += 1
    return
  }
  hard_delete_count.value = 0

  const url = new URL(`${curr_api}/media/delete`)
  url.searchParams.set('id', selected_media.value['id'])

  const result = await fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': token.uid,
      'Content-Type': 'application/json',
    }
  }).then(response => response.json())
  await get_media()
  selected_media.value = {}
}

async function add_media() {
  const token = await get_current_user()

  if (selected_media.value['user_rating'] === null) {
    added.value = 'false'
    return
  }

  const url = new URL(`${curr_api}/media/add`)

  const result = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': token.uid,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(selected_media.value)
  }).then(response => response.json())

  added.value = result.ok ? 'true' : 'false'
  setTimeout(()=>added.value = 'none',3000)
}

async function get_extra_posters() {
  const token = await get_current_user()

  const url = new URL(`${curr_api}/media/get_extra_posters`)

  url.searchParams.set('name', selected_media.value['name'])
  url.searchParams.set('external_id', selected_media.value['external_id'])
  url.searchParams.set('type', selected_media.value['media_type'])

  extra_posters.value = await fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': token.uid,
      'Content-Type': 'application/json',
    }
  }).then(response => response.json())
}

function replace_from_search(event) {
  delete event['id']
  delete event['user_rating']
  selected_media.value = {...selected_media.value, ...event}
  get_extra_posters()
  updated.value = 'none'
  added.value = 'none'
}

function insert_from_search(event) {
  selected_media.value = {...event}
  get_extra_posters()
  updated.value = 'none'
  added.value = 'none'
}

function handle_pane_close() {
  if (edit_pane_open.value) edit_pane_open.value = false
  if (add_pane_open.value) add_pane_open.value = false
}

function handle_key_press(e) {
  if (e.keyCode === 27) handle_pane_close()
  if (e.keyCode === 13 && e.ctrlKey) update_media()
}

function switch_poster(event) {
  selected_media.value['poster_path'] = event
}

onMounted(() => {
  if (selected_media.value['media_type']) search_type.value = selected_media.value['media_type']
  // console.log('selected', selected_media.value)
  if (add_pane_open.value) selected_media.value = {}

  fetch_filters()
  if (edit_pane_open.value) get_extra_posters()

  updated.value = 'none'
  added.value = 'none'
  window.addEventListener('keydown', handle_key_press)
})
onUnmounted(() => {
  window.removeEventListener('keydown', handle_key_press)
})
</script>

<template>
  <div class="edit_page_wrapper">

    <p>{{ added }}</p>

    <img @click="handle_pane_close" class="close_pane_button" alt="close_edit_pane"
         src="/ui/cross_button.png">

    <div v-if="add" class="search_area">

      <div style="display: flex;gap: 15px">
        <div class="search_bars">
          <!--          <div style="display: flex;align-items: center;gap: 10px">-->
          <!--            <h1>Library</h1>-->
          <!--            <filter-search style="height: 30px" @filter="get_media($event)" :auto_search="false"></filter-search>-->
          <!--          </div>-->
          <div style="display: flex;align-items: center;gap: 10px">
            <h1>Find</h1>
            <filter-search style="height: 30px" @filter="search_text=$event;find_media()"
                           :auto_search="false"></filter-search>
          </div>
        </div>

        <div class="media_type_selector">
          <label for="media_types" style="margin-right: 10px">Media type</label>
          <select v-model="search_type" id="media_types" @change="get_media();fetch_filters();">
            <option value="movie" :selected="search_type">movie</option>
            <option value="tv" :selected="search_type">tv</option>
            <option value="youtube" :selected="search_type">youtube</option>
            <option value="manga" :selected="search_type">manga</option>
            <option value="game" :selected="search_type">game</option>
          </select>
          <input v-model="search_page" type="number" style="margin-left: 10px;width: 50px" @change="find_media">
        </div>
      </div>
      <div class="search_result">
        <movie-container v-for="med in search_media"
                         :key="search_type + med['external_id'] + med['id']"
                         :data="med"
                         :container_size="container_size"
                         :scale_mul="0.6"
                         @media_data="replace_from_search"
        ></movie-container>
      </div>

    </div>

    <div class="preview_area">

      <div style="display:flex;flex-flow: column;gap: 20px;justify-content: space-between">

        <movie-container :data="selected_media"
                         :container_size="container_size"
                         :container_scale="0.35"
        ></movie-container>

        <div style="display: flex;flex-flow: column;align-content:space-evenly;gap:10px">
          <button v-if="edit" style="width: 100%;height: 65px" @click="update_media">Update</button>
          <img class="update_logo" alt="failed update" v-if="updated === 'false'"
               src="/ui/stop.png">
          <img class="update_logo" alt="failed update" v-if="updated === 'true'"
               src="/ui/success-green-check-mark-icon.svg">

          <button v-if="add" @click="add_media">Add</button>
          <img class="update_logo" alt="failed update" v-if="added === 'false'"
               src="/ui/stop.png">
          <img class="update_logo" alt="failed update" v-if="added === 'true'"
               src="/ui/success-green-check-mark-icon.svg">

          <button v-if="edit" @click="hard_delete">Hard delete</button>

        </div>
      </div>

      <div class="form_area">

        <div class="form_box">
          <label for="form_name">Name</label>
          <input id="form_name" v-model="selected_media['name']" type="text"
                 @change="selected_media['name']=$event.target.value">

          <label for="form_user_rating">Rating</label>
          <input id="form_user_rating" v-model="selected_media['user_rating']" type="number"
                 @change="selected_media['user_rating']=Number($event.target.value)">
          <div>
            <label for="form_user_dropped">dropped</label>
            <input id="form_user_dropped" v-model="selected_media['is_dropped']" type="checkbox"
                   @change="selected_media['is_dropped']=$event.target.checked">

            <label for="form_user_deleted">deleted</label>
            <input id="form_user_deleted" v-model="selected_media['is_deleted']" type="checkbox"
                   @change="selected_media['is_deleted']=$event.target.checked">
          </div>

          <label for="form_media_types">Content rating</label>
          <select v-if="selected_media['content_rating'] && selected_media['content_rating'].id"
                  @change="selected_media['content_rating']=content_ratings[$event.target.value]"
                  id="form_media_types">
            <option v-for="(c,i) in content_ratings" :key="c['id']" :value="i"
                    :selected="selected_media['content_rating'].id === c.id">
              {{ c.name }}
            </option>
            .value
          </select>

          <label for="form_media_types">All Content ratings</label>
          <select @change="selected_media['content_rating']=all_content_ratings[$event.target.value]"
                  id="form_media_types"
          >
            <option v-for="(c,i) in all_content_ratings" :key="c['id']" :value="i">
              {{ c.name }}
            </option>
            .value
          </select>


          <label for="form_image_url">Poster path</label>
          <textarea id="form_image_url" v-model="selected_media['poster_path']"
                    style="width: 100%"
                    @change="selected_media['poster_path']=$event.target.value"></textarea>

          <label for="form_external_link">External link</label>
          <textarea id="form_external_link" v-model="selected_media['external_link']"
                    style="width: 100%"
                    @change="selected_media['external_link']=$event.target.value"></textarea>

          <label for="form_public_rating">Public rating</label>
          <input id="form_public_rating" v-model="selected_media['public_rating']" type="number"
                 @change="selected_media['public_rating']=$event.target.value">

          <!--          <label for="form_added_date">Date added</label>-->
          <!--          <input id="form_added_date" v-model="selected_media['created_at']" type="text"-->
          <!--                 @change="selected_media['created_at']=$event.target.value">-->

        </div>

      </div>

      <div class="tier_list_area">
        <tier-list-picker></tier-list-picker>
      </div>

      <div class="extra_posters">
        <div class="extra_poster" v-for="poster in extra_posters" :key="poster">
          <img :src="poster" alt="extra_poster" class="extra_poster_image" @click="switch_poster(poster)">
        </div>
      </div>

    </div>

    <div class="tags_area">
      <tag-picker :media_type="search_type"></tag-picker>
    </div>

  </div>
</template>

<style scoped>
.edit_page_wrapper {
  overflow-y: scroll;
  border: 2px dotted #464646;
  padding: 10px;
  display: flex;
  flex-flow: column nowrap;
  /*gap: 10px;*/
  height: 100%;

}

.search_area {
  padding: 20px;
  display: flex;
  flex-flow: column wrap;
  gap: 15px;
}

.search_bars {
  display: flex;
  flex-flow: column;
  gap: 10px;
}

.preview_area {
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  /*flex-flow: row;*/
  gap: 20px;
}

.form_area {
  display: flex;
  flex-flow: column wrap;
  gap: 10px;
  justify-content: space-between;
}

.tier_list_area {
  display: flex;
  flex-flow: column wrap;
  gap: 10px;
  /*justify-content: space-between;*/
}

.form_box {
  display: flex;
  flex-flow: column;
  gap: 10px;
  align-items: flex-start;
}

.extra_posters {
  border: 2px dotted #464646;
  min-width: 50px;

  display: flex;
  flex-flow: row wrap;
  gap: 5px;
  overflow-y: scroll;
  height: 500px;
}

.extra_poster_image {
  /*width: 150px;*/
  height: 150px;
  object-fit: contain;
}

.search_result {
  overflow-x: scroll;
  display: flex;
  flex-flow: row;
  gap: 10px;
}

.update_logo {
  height: 20px;
}

.close_pane_button {
  cursor: pointer;
  position: absolute;
  filter: invert();
  right: 5px;
  top: 5px;
  width: 20px;
  object-fit: contain;
}
</style>