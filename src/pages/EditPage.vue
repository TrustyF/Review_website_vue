<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import FilterSearch from "@/components/media_filters/filterSearch.vue";
import MovieContainer from "@/components/media_container/movie_container/MovieContainer.vue";

let props = defineProps(["test"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

let search_type = ref('movie')

let search_media = ref()
let selected_media = ref({})
let extra_posters = ref([])
let form_bindings = ref([
  {
    'name': 'text',
    'media_type': 'text',
    'media_medium': 'text',
  },
  {
    'user_rating': 'number',
    // 'public_rating': 'number',
  },
  {
    'is_dropped': 'checkbox',
    'is_deleted': 'checkbox',
  },
  {
    // 'episodes': 'number',
    // 'seasons': 'number',
    'content_rating': 'text',
  }
])
let form_changes = ref({})

let updated = ref(false)
let added = ref(false)

async function get_media(text) {

  const url = new URL(`${curr_api}/media/get`)
  const params = {
    'limit': 5,
    'page': 0,
    'session_seed': 1,
    'search': text,
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

}

async function find_media(text) {

  const url = new URL(`${curr_api}/media/find`)
  url.searchParams.set('name', text)
  url.searchParams.set('type', search_type.value)

  search_media.value = await fetch(url).then(response => response.json())
  console.log(search_media.value)
}

async function update_media() {

  if (form_changes.value['id'] === undefined) return
  if (Object.keys(form_changes.value).length < 2) return

  form_changes.value['id'] = selected_media.value['id']

  const url = new URL(`${curr_api}/media/update`)

  const result = await fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(form_changes.value)
  }).then(response => response.json())

  updated.value = result.ok
}

async function add_media() {
  const url = new URL(`${curr_api}/media/add`)

  const result = await fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(selected_media.value)
  }).then(response => response.json())

  added.value = result.ok
}

async function get_extra_posters() {

  const url = new URL(`${curr_api}/media/get_extra_posters`)

  url.searchParams.set('name', selected_media.value['name'])
  url.searchParams.set('external_id', selected_media.value['external_id'])
  url.searchParams.set('type', selected_media.value['media_type'])

  extra_posters.value = await fetch(url).then(response => response.json())
}

function handleMediaEmit(event) {
  selected_media.value = event
  form_changes.value = {'id': event['id']}
  get_extra_posters()
  updated.value = false
  added.value = false
}

function switch_poster(event) {
  form_changes.value['poster_path'] = event
  selected_media.value['poster_path'] = event
}

onMounted(() => {
  get_media()
})
</script>

<template>
  <div class="edit_page_wrapper">

    <div class="search_area">

      <div class="search_bars">
        <h1>Library</h1>
        <filter-search @filter="get_media($event)"></filter-search>
        <h1>Find</h1>
        <filter-search @filter="find_media($event)"></filter-search>
      </div>

      <div class="search_result">
        <movie-container v-for="med in search_media"
                         :key="med['id']"
                         :data="med"
                         :container_size="[500,750]"
                         :container_scale="0.20"
                         @media_data="handleMediaEmit"
        ></movie-container>
      </div>
    </div>

    <div class="preview_area">
      <movie-container :data="selected_media"
                       :container_size="[500,750]"
                       :container_scale="0.35"
                       @media_data="handleMediaEmit"
      ></movie-container>

      <div class="form_area">

        <div class="form_group" v-for="group in form_bindings" :key="group">
          <div class="form_box" v-for="(key) in Object.keys(group)" :key="key">
            <label :for="key">{{ key }}</label>

            <input v-if="group[key]!=='checkbox'"
                   v-model="selected_media[key]"
                   :type="group[key]"
                   @change="form_changes[key]=$event.target.value">
            <input v-else
                   v-model="selected_media[key]"
                   type="checkbox"
                   @change="form_changes[key]=$event.target.checked">
          </div>
        </div>

        <div style="display: flex;align-items: center;gap:10px">
          <button style="width: 100px" @click="update_media">Update</button>
          <button style="width: 100px" @click="add_media">Add</button>
          <img class="update_logo" alt="success update" v-if="updated || added"
               src="src/assets/ui/success-green-check-mark-icon.svg">
        </div>

        <p style="font-size: 0.6em">{{ form_changes }}</p>

      </div>

      <div class="extra_posters">
        <div class="extra_poster" v-for="poster in extra_posters" :key="poster">
          <img :src="poster" alt="extra_poster" class="extra_poster_image" @click="switch_poster(poster)">
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.edit_page_wrapper {
  display: flex;
  flex-flow: column nowrap;
  /*gap: 10px;*/
}

.search_area {
  padding: 20px;
  display: flex;
  flex-flow: column;
  gap: 15px;
}

.search_bars {
  display: grid;
  grid-template-rows: 1fr;
}

.preview_area {
  padding: 20px;
  display: flex;
  flex-flow: row;
  gap: 20px;
}

.form_area {
  display: flex;
  flex-flow: column wrap;
  gap: 10px;
  justify-content: space-between;
}

.form_box {
  display: grid;
  gap: 5px;
  /*align-items: center;*/
}

.extra_posters {
  display: flex;
  flex-flow: row wrap;
  gap: 5px;
  overflow-y: scroll;
  height: 400px;
  /*width: 600px;*/
}

.extra_poster_image {
  width: 150px;
  height: 200px;
  object-fit: contain;
}

.search_result {
  display: flex;
  flex-flow: row wrap;
  gap: 10px;
}

.update_logo {
  height: 20px;
}
</style>