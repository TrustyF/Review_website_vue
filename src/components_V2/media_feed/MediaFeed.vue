<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import blue_star from '/src/assets/ui/blue_star.png'

let props = defineProps(["media_type", "media_container","media_scale","media_size"]);

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

async function get_media() {

  const url = new URL(`${curr_api}/media/get`)

  url.searchParams.set('limit', String(media_limit.value))
  url.searchParams.set('page', String(media_page.value))
  url.searchParams.set('order', media_order.value)
  url.searchParams.set('session_seed', String(session_seed))

  url.searchParams.set('type', props['media_type'])

  const result = await fetch(url).then(response => response.json())

  // skip if no data returned
  if (result.length < 1) {
    return
  }

  // concat result to media
  result.forEach(entry => media.value.push(entry))
  // group media
  media_grouped.value = media.value.reduce((r, e, index) => {
    if (!r[e['user_rating']]) r[e['user_rating']] = [e]
    else r[e['user_rating']].push(e)
    return r;
  }, {})

  // cleanup
  is_loading_more_media.value = false
  scroll_media_loader()

}

function scroll_media_loader() {
  let rect = document.getElementById('media_container').getBoundingClientRect()

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
  addEventListener("scroll", () => scroll_media_loader())
  addEventListener("resize", () => check_mobile())
})

</script>

<template>

  <div id="media_container">
    <div class="rating_box" v-for="rating in Object.keys(media_grouped).reverse()" :key="rating">

      <div class="rating_separator">
        <h1 style="height: 0.8em;font-weight: 500;font-size: 1em"> {{ rating }} </h1>
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

.rating_box {
  position: relative;
}

.rating_separator {
  /*outline: 1px solid red;*/
  width: fit-content;
  padding: 10px;
  margin: 50px 0 15px 0;
  background-color: #2d2d41;
  border-radius: 8px;
  position: sticky;
  top: 10px;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 3px;
}

.rating_separator_mobile {
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