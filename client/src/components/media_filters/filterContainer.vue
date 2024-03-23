<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import FilterDropdown from "@/components/media_filters/filterDropdown.vue";
import FilterRange from "@/components/media_filters/filterRange.vue";
import FilterRadio from "@/components/media_filters/filterRadio.vue";
import axios from "axios";

let props = defineProps({
  media_types: {
    default: () => [],
    type: Array
  },
  tier_lists: {
    default: null,
    type: Array
  }
});

let emits = defineEmits(["filter"]);
const curr_api = inject("curr_api");
const vis_container_content_rating = inject("vis_container_content_rating");

let genres = ref(null)
let themes = ref(null)
let tags = ref(null)
let content_ratings = ref(null)
let difficulty = ref([
  {'id': 1, 'name': 'Accessible', 'value': 'name'},
  {'id': 2, 'name': 'Involved', 'value': 'release_date'},
  {'id': 3, 'name': 'Difficult', 'value': 'public_rating'},
])

let user_ratings = ref([0, 0])
let public_ratings = ref([0, 0])
let release_dates = ref([0, 0])
let runtimes = ref([0, 0])
let orders = ref([
  {'id': 0, 'name': 'Name', 'value': 'name'},
  {'id': 1, 'name': 'Release date', 'value': 'release_date'},
  {'id': 2, 'name': 'Public rating', 'value': 'public_rating'},
  {'id': 3, 'name': 'Runtime', 'value': 'runtime'},
  {'id': 4, 'name': 'Date added', 'value': 'date_added'},
])
let options = ref([
  {'id': 0, 'name': 'Show content ratings', 'value': vis_container_content_rating},
])

function handle_options(event) {
  // console.log(event.value)

  if (event.value.length < 1) {
    options.value.forEach((option) => {
      option['value'] = false
    })
  } else {
    event.value.forEach((event_id) => {
      options.value[event_id]["value"] = !options.value[event_id]["value"]
    })
  }
}

async function fetch_filters() {

  const url = new URL(`${curr_api}/media/get_filters`)
  const params = {
    'types': props['media_types'],
    'tier_lists': props['tier_lists'],
  }

  const result = await axios(
      {
        method: 'POST',
        url: url,
        headers: {"Content-Type": "application/json"},
        data: JSON.stringify(params)
      })
      .then(response => response.data)
      .catch(error => {
        // console.log('fetch_filters', error.response)
        return []
      })

  // console.log('filters', result)

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
  content_ratings.value.map((x) => x['name'] += `: +${x['age']}`)

  // console.log(content_ratings.value)

}

function emit_filter(title, event) {
  // console.log(title, event.value)
  emits('filter', [title, event])
}

onMounted(() => {
  fetch_filters()
})
</script>

<template>
  <div class="filter_inner_container_wrapper">

    <div class="col">
      <filter-dropdown @id="handle_options"
                       :data="options" title="Options"></filter-dropdown>
    </div>

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
      <filter-dropdown v-if="difficulty!==null && difficulty.length>0"
                       @id="emit_filter('difficulty',$event)"
                       :data="difficulty" title="Difficulty"></filter-dropdown>
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
  grid-template-columns: repeat(3, 1fr);

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