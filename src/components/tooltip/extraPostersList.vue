<script setup>
import {inject, ref, watch} from "vue";
import {get_current_user} from "@/firebase_auth";

let props = defineProps(['selected_media']);
let emits = defineEmits(["picked_poster"]);
const curr_api = inject("curr_api");

let extra_posters_rows = ref(1.5)
let extra_posters = ref([])

function proxy_image(path) {
  if (path === undefined) return ''
  return `${curr_api}/media/proxy_poster?path=${path}`
}

function emit_poster(path) {
  emits('picked_poster', path)
}

async function get_extra_posters() {
  if (!props["selected_media"].name) return

  const token = await get_current_user()

  const url = new URL(`${curr_api}/media/get_extra_posters`)

  url.searchParams.set('name', props["selected_media"]['name'])
  url.searchParams.set('external_id', props["selected_media"]['external_id'])
  url.searchParams.set('type', props["selected_media"]['media_type'])

  extra_posters.value = await fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': token.uid,
      'Content-Type': 'application/json',
    }
  }).then(response => response.json())
}

watch(() => props.selected_media, () => {
  console.log('getting')
  get_extra_posters()
}, {immediate: true})
</script>

<template>
  <div class="extra_posters">

    <input type="range" step="0.5" min="0.5" max="2" v-model="extra_posters_rows"
           style="position:absolute;left: 0;bottom: 0;width: 50%">

    <div class="extra_posters_list">
      <div class="extra_poster" v-for="poster in extra_posters" :key="poster">
        <img v-lazy="proxy_image(poster)" alt="extra_poster" class="extra_poster_image"
             @click="emit_poster(poster)">
      </div>
    </div>
  </div>
</template>

<style scoped>
.extra_posters {
  position: relative;
  border: 2px dotted #464646;
  min-width: 50px;

  height: 595px;
}
.extra_posters_list {
  height: 100%;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(calc(70px * v-bind(extra_posters_rows)), 1fr));
  overflow-y: scroll;
}
.extra_poster_image {
  height: 100%;
  width: 100%;
  object-fit: contain;
}
</style>