<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import FilterSearch from "@/components/media_filters/filterSearch.vue";
import MovieContainer from "@/components/media_container/movie_container/MovieContainer.vue";

let props = defineProps(["test"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

let search_media = ref()
let selected_media = ref({})
let form_bindings = ref([
  {
    'name': 'text',
    'media_type': 'text',
    'media_medium': 'text',
  },
  {
    'user_rating': 'number',
    'public_rating': 'number',
  },
  {
    'is_dropped': 'checkbox',
    'is_deleted': 'checkbox',
  },
  {
    'runtime': 'number',
    'episodes': 'number',
    'seasons': 'number',
    'content_rating': 'text',
  }
])
let form_changes = ref({})

let updated = ref(false)

async function get_media(text) {

  const url = new URL(`${curr_api}/media/get`)
  const params = {
    'limit': 5,
    'page': 0,
    'session_seed': 1,
    'search': text,
  }

  search_media.value = await fetch(url,
      {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(params)
      })
      .then(response => response.json())

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

function handleMediaEmit(event) {
  selected_media.value = event
  form_changes.value = {'id': event['id']}
  updated.value = false
}

function remove_form_key(key){
  delete form_changes.value[key]
}

onMounted(() => {
  get_media('drag')
})
</script>

<template>
  <div class="edit_page_wrapper">

    <div class="search_area">
      <filter-search @filter="get_media($event)"></filter-search>

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
        <p>{{ form_changes }}</p>

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
                   @change="form_changes[key]=$event.target.checked ? true : remove_form_key(key)">
          </div>
        </div>
        <div style="display: flex;align-items: center;gap:10px">
        <button style="width: 100px" @click="update_media">Update</button>
        <img class="update_logo" alt="success update" v-if="updated" src="src/assets/ui/success-green-check-mark-icon.svg">
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
  gap: 15px;
  justify-content: space-between;
}

.form_box {
  display: flex;
  gap: 5px;
  align-items: center;
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