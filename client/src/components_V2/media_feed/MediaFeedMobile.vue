<script setup>
import {inject, onMounted, watch, ref, computed, onUnmounted} from "vue";
import blue_star from '/src/assets/ui/blue_star.png'

let props = defineProps(["media_type", "media_container", "media_scale", "media_size"]);

const curr_api = inject("curr_api");
const session_seed = inject("session_seed");

const element_width = computed(() => String(props['media_size'][0] * props['media_scale']) + 'px')

let media = ref([])
let media_grouped = ref([])

let media_limit = ref(5)
let media_page = ref(0)
let media_order = ref(undefined)

let is_loading_more_media = ref(false)
let is_all_media_loaded = ref(false)
let is_mobile = ref(false)

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
  }
  console.log('fetching')

  const result = await fetch(url,
      {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(params)
      })
      .then(response => response.json())

  // mark page loaded if no data returned
  if (result.length < 1) {
    console.log('page finished loading')
    is_page_loading.value = false
    is_page_loaded.value = true
  }

  if (override) {
    console.log('overriding')
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

function scroll_media_loader() {
  let elem = document.getElementById('media_container')
  if (elem === null) return

  let rect = elem.getBoundingClientRect()

  if (rect.bottom <= (window.innerHeight + (window.innerHeight / 2)) &&
      !is_loading_more_media.value &&
      !is_all_media_loaded.value) {

    console.log('loading more media')
    is_loading_more_media.value = true
    media_page.value += 1
    get_media()
  }
}

function check_mobile() {
  // console.log(document.body.clientWidth)
  is_mobile.value = document.body.clientWidth < 500;
}

onMounted(() => {
  get_media()
  check_mobile()
  window.addEventListener("scroll", () => scroll_media_loader())
  window.addEventListener("resize", () => check_mobile())
})

onUnmounted(() => {
  window.removeEventListener("scroll", () => scroll_media_loader())
  window.removeEventListener("resize", () => check_mobile())
})

</script>

<template>

  <div id="media_container">
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
  gap: 10px;
  justify-items: center;
  display: flex;
  flex-flow: column nowrap;
}

.rating_box {
  position: relative;
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

</style>