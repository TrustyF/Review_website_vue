<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import FilterDropdown from "@/components_V2/media_filters/filterDropdown.vue";
import FilterRange from "@/components_V2/media_filters/filterRange.vue";

let props = defineProps(["media_type"]);
let emits = defineEmits(["filter"]);
const curr_api = inject("curr_api");

let genres = ref()
let themes = ref()
let tags = ref()
let ratings = [1, 9]
let public_ratings = [1, 9]
let release_date = [1900, 2024]
let runtime = [0, 250]

async function fetch_filters() {

  const url = new URL(`${curr_api}/media/get_filters`)
  url.searchParams.set('type', props['media_type'])

  const result = await fetch(url).then(response => response.json())
  console.log('filters', result)

  genres.value = result['genres']
  themes.value = result['themes']
  tags.value = result['tags']
  tags.value.sort((a, b) => a['tier'] > b['tier'])

}

function emit_filter(title, event) {
  emits('filter', [title, event])
}

onMounted(() => {
  fetch_filters()
})
</script>

<template>
  <div class="filter_container_wrapper">

    <filter-dropdown @id="emit_filter('tags',$event)" :data="tags" title="Tags"></filter-dropdown>

    <filter-dropdown @id="emit_filter('genres',$event)" :data="genres" title="Genres"></filter-dropdown>
    <filter-dropdown @id="emit_filter('themes',$event)" v-if="themes!==undefined && themes.length>0"
                     :data="themes" title="Themes"></filter-dropdown>

    <filter-range @values="emit_filter('ratings',$event)" :data="ratings" title="Ratings"></filter-range>
    <filter-range @values="emit_filter('public_ratings',$event)" :data="public_ratings"
                  title="Public ratings"></filter-range>

    <filter-range @values="emit_filter('release_dates',$event)" :data="release_date"
                  title="Release date"></filter-range>

    <filter-range @values="emit_filter('runtimes',$event)" :data="runtime"
                  title="Runtime" :time="true"></filter-range>
  </div>
</template>

<style scoped>
.filter_container_wrapper {
  display: flex;
  flex-flow: column wrap;
  align-content: flex-start;
  outline: 1px solid orange;
  padding: 10px;
  /*width: 500px;*/
  height: 500px;
  gap: 20px;
  background-color: black;

  z-index: 100;
}
</style>