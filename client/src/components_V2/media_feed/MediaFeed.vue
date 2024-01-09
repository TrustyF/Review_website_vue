<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import blue_star from '/src/assets/ui/blue_star.png'
import FilterContainer from "@/components_V2/media_filters/filterContainer.vue";

let props = defineProps(["media_type", "media_container", "media_scale", "media_size"]);

const curr_api = inject("curr_api");
const session_seed = inject("session_seed");

const element_width = computed(() => String(props['media_size'][0] * props['media_scale']) + 'px')

let media = ref([])
let media_grouped = ref([])

let media_limit = ref(5)
let media_page = ref(0)
let media_order = ref(undefined)
let media_filters = ref({})

let feed_container = ref()

let is_page_loaded = ref(false)
let is_page_loading = ref(true)

async function get_media() {

  const url = new URL(`${curr_api}/media/get`)
  const params = {
    'limit': media_limit.value,
    'page': media_page.value,
    'order': media_order.value,
    'session_seed': session_seed,
    'type': props['media_type'],
    'genres': media_filters.value['genres'],
    'themes': media_filters.value['themes'],
    'tags': media_filters.value['tags'],
  }

  const result = await fetch(url,
      {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(params)
      })
      .then(response => response.json())

  // skip if no data returned
  if (result.length < 1) {
    console.log('page finished loading')
    return
  }

  // concat result to media
  result.forEach(entry => media.value.push(entry))
  // group media by rating
  media_grouped.value = media.value.reduce((r, e, index) => {
    if (!r[e['user_rating']]) r[e['user_rating']] = [e]
    else r[e['user_rating']].push(e)
    return r;
  }, {})

  console.log('grouped movies', media_grouped.value)

  // cleanup
  is_page_loading.value = false
  handleInfiniteScroll()

}

function handle_filter(event) {
  console.log('event', event)
  media_filters.value = event
  clean_load_media()
}

const handleInfiniteScroll = () => {
  if (is_page_loading.value) {
    console.log('page busy loading, skipping')
    return;
  }
  let container = feed_container.value
  if (container === null) {
    return
  }

  let container_bot = container.getBoundingClientRect()

  const endOfPage = (window.innerHeight + 400) >= container_bot.bottom;

  if (endOfPage && !is_page_loading.value && !is_page_loaded.value) {
    is_page_loading.value = true
    media_page.value += 1
    get_media()
    console.log('loading more', media_page.value)
  }

};

function clean_load_media() {
  media_page.value = 0
  media.value = []
  media_grouped.value = []
  is_page_loaded.value = false
  get_media()
}

onMounted(() => {
  get_media()
  addEventListener("scroll", () => handleInfiniteScroll())
})

</script>

<template>

  <div class="filter_wrapper">
    <filter-container @filter="handle_filter" :media_type="media_type"></filter-container>
  </div>

  <div ref="feed_container">
    <div class="rating_box" v-for="rating in Object.keys(media_grouped).reverse()" :key="rating">

      <div class="rating_separator">
        <h1 style="font-weight: 500;font-size: 1em"> {{ rating }} </h1>
        <img :src="blue_star" alt="blue_star" style="width: 15px">
      </div>

      <div class="media_container_wrapper">
        <component v-for="med in media_grouped[rating]"
                   :key="med['id']"
                   :is="media_container"
                   :data="med"
                   :container_size="media_size"
                   :container_scale="media_scale"></component>
      </div>

    </div>
  </div>

</template>

<style scoped>

.media_container_wrapper {
  gap: 20px;

  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(v-bind(element_width), 1fr));
}

.filter_wrapper {
  position: relative;
}

.rating_box {
  position: relative;
}

.rating_separator {
  width: fit-content;
  padding: 10px;
  margin: 50px 0 15px 0;
  background-color: #2d2d41;
  box-shadow: 0 0 5px #000000;
  border-radius: 8px;
  position: sticky;
  top: 10px;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 3px;
}

</style>