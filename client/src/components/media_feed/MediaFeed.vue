<script setup>
import {inject, onMounted, watch, provide, ref, computed} from "vue";
import blue_star from '/src/assets/ui/blue_star.png'
import MovieContainer from "@/components/media_container/movie_container/MovieContainer.vue";
import MovieContainerMobile from "@/components/media_container/movie_container/MovieContainerMobile.vue";
import MediaFeedFilterBar from "@/components/media_feed/MediaFeedFilterBar.vue";

let props = defineProps(["media_type", "media_scales", "media_sizes"]);

const curr_api = inject("curr_api");
const session_seed = inject("session_seed");
const is_mobile = inject("is_mobile");

let media_scale = computed(() => is_mobile.value ? props['media_scales'][1] : props['media_scales'][0])
let media_size = computed(() => is_mobile.value ? props['media_sizes'][1] : props['media_sizes'][0])
let media_container = computed(() => is_mobile.value ? MovieContainerMobile : MovieContainer)

const element_width = computed(() => String(media_size.value[0] * media_scale.value) + 'px')

let media = ref([])
let media_grouped = ref([])

let media_limit = ref(20)
let media_page = ref(0)
let media_order = ref(undefined)
let media_filters = ref({})

let feed_container = ref()

let is_page_loaded = ref(false)
let is_page_loading = ref(true)


async function get_media(override) {

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
    'ratings': media_filters.value['ratings'],
    'public_ratings': media_filters.value['public_ratings'],
    'release_dates': media_filters.value['release_dates'],
    'runtimes': media_filters.value['runtimes'],
    'search': media_filters.value['search'],
  }

  const result = await fetch(url,
      {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(params)
      })
      .then(response => response.json())

  // mark page loaded if no data returned
  if (result.length < 1) {
    is_page_loading.value = false
    is_page_loaded.value = true
  }

  if (override) {
    media.value = result
  } else {
    // concat result to media
    result.forEach(entry => media.value.push(entry))
  }

  // group media by rating
  media_grouped.value = media.value.reduce((r, e, index) => {
    if (!r[e['user_rating']]) r[e['user_rating']] = [e]
    else r[e['user_rating']].push(e)
    return r;
  }, {})

  // cleanup
  is_page_loading.value = false
  handleInfiniteScroll()

}

function handle_filter(event) {
  console.log('event', event)
  media_filters.value[event[0]] = event[1]
  clean_load_media()
}

const handleInfiniteScroll = () => {
  if (is_page_loading.value) {
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
    // console.log('loading more', media_page.value)
  }

};

function clean_load_media() {
  media_page.value = 0
  is_page_loaded.value = false
  get_media(true)
}

onMounted(() => {
  get_media()
  addEventListener("scroll", () => handleInfiniteScroll())
})

</script>

<template>
  <!--  <p style="position: fixed;left: 0;z-index: 1000;background-color: black">{{`is_page_loaded=${is_page_loaded}`}}</p>-->
  <!--  <p style="position: fixed;left: 0;top: 100px;z-index: 1000;background-color: black">{{`is_page_loading=${is_page_loading}`}}</p>-->

  <div class="top_feed_container" ref="feed_container">

    <media-feed-filter-bar @filter="handle_filter" :media_type="media_type"></media-feed-filter-bar>

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

    <div v-if="media.length < 1" class="empty_result">No result</div>

  </div>

</template>

<style scoped>
.top_feed_container {
  min-height: 100px;
}

.media_container_wrapper {
  gap: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(v-bind(element_width), 1fr));
}

.rating_box {
  position: relative;
  margin: 0 0 40px 0;
}

.rating_separator {
  width: fit-content;
  padding: 10px;
  margin: 0 0 25px 0;
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

.empty_result {
  position: relative;
  text-align: center;
  margin-top: 100px;
  padding-bottom: 100px;
}

@media only screen and (max-width: 500px) {
  .media_container_wrapper {
    gap: 10px;
    justify-items: center;
    display: flex;
    flex-flow: column nowrap;
  }

  .rating_separator {
    /*outline: 1px solid red;*/
    width: fit-content;
    padding: 7px;
    margin: 35px 0 5px 0;
    background-color: #2d2d41;
    border-radius: 8px;
    position: sticky;
    top: 10px;
    z-index: 5;
    display: flex;
    align-items: center;
    gap: 3px;
  }
}

</style>