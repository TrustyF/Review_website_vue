<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import FilterDropdown from "@/components_V2/media_filters/filterDropdown.vue";

let props = defineProps(["media_type"]);
let emits = defineEmits(["filter"]);
const curr_api = inject("curr_api");

let genres = ref()
let themes = ref()
let tags = ref()

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

  let obj = {}
  obj[title] = event

  emits('filter', obj)
}

onMounted(() => {
  fetch_filters()
})
</script>

<template>
  <div class="filter_wrapper">

    <filter-dropdown @id="emit_filter('genres',$event)" :data="genres" title="Genres"></filter-dropdown>
    <filter-dropdown @id="emit_filter('themes',$event)" v-if="themes!==undefined && themes.length>0"
                     :data="themes" title="Themes"></filter-dropdown>
    <filter-dropdown @id="emit_filter('tags',$event)" :data="tags" title="Tags"></filter-dropdown>

  </div>
</template>

<style scoped>
.filter_wrapper {
  display: flex;
  /*width: 500px;*/
  height: 500px;
  background-color: black;

  z-index: 100;
}
</style>