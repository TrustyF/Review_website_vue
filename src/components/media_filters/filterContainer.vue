<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import FilterDropdown from "@/components/media_filters/filterDropdown.vue";
import FilterRange from "@/components/media_filters/filterRange.vue";
import FilterRadio from "@/components/media_filters/filterRadio.vue";
import {check_server_awake} from "@/utils.js";

let props = defineProps(["media_type", "tier_lists"]);
let emits = defineEmits(["filter"]);
const curr_api = inject("curr_api");

let genres = ref(null)
let themes = ref(null)
let tags = ref(null)
let content_ratings = ref(null)

let user_ratings = ref([0, 0])
let public_ratings = ref([0, 0])
let release_dates = ref([0, 0])
let runtimes = ref([0, 0])
let orders = ref([
  {'id': 1, 'name': 'Name', 'value': 'name'},
  {'id': 0, 'name': 'Release date', 'value': 'release_date'},
  {'id': 2, 'name': 'Public rating', 'value': 'public_rating'},
  {'id': 3, 'name': 'Runtime', 'value': 'runtime'},
  {'id': 4, 'name': 'Date added', 'value': 'date_added'},
])

async function fetch_filters() {

  // if (!await check_server_awake(curr_api)) return

  const url = new URL(`${curr_api}/media/get_filters`)
  const params = {
    'type': props['media_type'] !== undefined ? props['media_type'] : '',
    'tier_lists': props['tier_lists'] !== undefined ? props['tier_lists'] : [],
  }


  const result = await fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(params)
  }).then(response => response.json())

  console.log('filters', result)

  genres.value = result['genres']
  themes.value = result['themes']
  tags.value = result['tags']
  tags.value.sort((a, b) => a['tier'] > b['tier'])

  user_ratings.value = result['user_ratings']
  public_ratings.value = result['public_ratings']
  release_dates.value = result['release_dates']
  runtimes.value = result['runtimes']

  content_ratings.value = result['content_ratings']
  content_ratings.value.sort((a, b) => a['order'] > b['order'])
}

function emit_filter(title, event) {
  emits('filter', [title, event])
}

onMounted(() => {
  fetch_filters()
})
</script>

<template>
  <div class="filter_inner_container_wrapper">
    <div class="ranges_box">
      <filter-range v-if="user_ratings[0] !== user_ratings[1]"
                    @values="emit_filter('ratings',$event)"
                    :data="user_ratings" title="My rating"></filter-range>
      <filter-range v-if="public_ratings[0] !== public_ratings[1]"
                    @values="emit_filter('public_ratings',$event)"
                    :data="public_ratings"
                    title="Public rating" :step="1"></filter-range>
      <filter-range v-if="release_dates[0] !== release_dates[1]"
                    @values="emit_filter('release_dates',$event)"
                    :data="release_dates"
                    title="Release date"></filter-range>
      <filter-range v-if="runtimes[0] !== runtimes[1]"
                    @values="emit_filter('runtimes',$event)"
                    :data="runtimes"
                    title="Runtime" :time="true" :step="15"></filter-range>
    </div>


    <div class="col">
      <filter-radio v-if="orders!==null && orders.length>0"
                    @value="emit_filter('order',$event)"
                    :data="orders" title="Sort by"></filter-radio>
      <filter-dropdown v-if="content_ratings!==null && content_ratings.length>0"
                       @id="emit_filter('content_ratings',$event)"
                       :data="content_ratings" title="Content rating"></filter-dropdown>
    </div>

    <div class="col">
      <filter-dropdown v-if="tags !== null && tags.length>0"
                       @id="emit_filter('tags',$event)"
                       :data="tags" title="Tags"></filter-dropdown>

      <filter-dropdown v-if="genres !== null && genres.length>0"
                       @id="emit_filter('genres',$event)"
                       :data="genres" title="Genres"></filter-dropdown>
    </div>

    <div class="col">
    <filter-dropdown v-if="themes!==null && themes.length>0"
                     @id="emit_filter('themes',$event)"
                     :data="themes" title="Themes"></filter-dropdown>
    </div>



  </div>
</template>

<style scoped>
.filter_inner_container_wrapper {
  position: relative;
  /*outline: 2px solid orange;*/
  margin: 20px;

  height: 100%;
  display: flex;
  flex-flow: column;
  gap: 20px;
}

.genres_box {
  /*outline: 2px solid greenyellow;*/
  width: 100%;
  display: flex;
  flex-flow: row;
  gap: 10px;

  justify-content: space-evenly;
  /*align-content: center;*/
}

.col {
  /*outline: 2px solid red;*/
  display: grid;
  grid-template-columns: repeat(2, 1fr);

  gap: 10px;
}

.ranges_box {
  /*outline: 3px solid greenyellow;*/
  display: flex;
  flex-flow: row;
  gap: 10px;

  /*margin: 20px;*/

  padding: 20px;
  background-color: #131215;
  border-radius: 10px;
  filter: drop-shadow(1px 1px 3px black);
}

@media only screen and (max-width: 500px) {
  .genres_box {
    flex-flow: row wrap;
  }

  .ranges_box {
    flex-flow: column;
  }
}
</style>