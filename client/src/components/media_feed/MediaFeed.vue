<script setup>
import {inject, onMounted, watch, provide, ref, computed, onUnmounted} from "vue";
import blue_star from '/ui/blue_star.png'
import MovieContainer from "@/components/media_container/movie_container/MovieContainer.vue";
import MovieContainerMobile from "@/components/media_container/movie_container/MovieContainerMobile.vue";
import MediaFeedFilterBar from "@/components/media_feed/MediaFeedFilterBar.vue";
import CreditsFooter from "@/components/General/CreditsFooter.vue";
import spinner from '/ui/custom_spinner.webp'
import axios from "axios";

let props = defineProps({
  media_types: {
    default: null,
    type: Array,
  },
  media_container_type: {
    default: 'movie',
    type: String,
  },
  media_container_type_override: {
    default: null,
    type: String,
  },
  tier_lists: {
    default: null,
    type: Array,
  },
});

const curr_api = inject("curr_api");
const edit_mode = inject("edit_mode");
const session_seed = inject("session_seed");
const is_mobile = inject("is_mobile");
let selected_media = inject('selected_media')
let edit_pane_open = inject('edit_pane_open')
let is_visible_navbar = inject('is_visible_navbar')
let media_scales = inject('media_scales')

let media_container = computed(() => {
  if (is_mobile.value) {
    return MovieContainerMobile
  } else {
    return MovieContainer
  }
})
const element_width = computed(() => {
  return String(media_scales.value[props.media_container_type]['size'][0] *
      media_scales.value[props.media_container_type]['scale']) + 'px'
})

let media = ref([])
let media_grouped = ref([])

let media_limit = ref(20)
let media_page = ref(0)
let media_filters = ref({})
let filter_load_status = ref('none')
let page_load_status = ref('none')
let search_matched_field = ref('')

let feed_container = ref()

let is_page_loaded = ref(false)
let is_page_loading = ref(true)

let vis_container_content_rating = ref(false)
provide('vis_container_content_rating', vis_container_content_rating)

async function get_media(override) {

  const url = new URL(`${curr_api}/media/get`)
  const params = {
    'limit': media_limit.value,
    'page': media_page.value,
    'session_seed': session_seed,
    'types': props['media_types'],
    'genres': media_filters.value['genres'],
    'themes': media_filters.value['themes'],
    'tags': media_filters.value['tags'],
    'tier_lists': props['tier_lists'],
    'ratings': media_filters.value['ratings'],
    'public_ratings': media_filters.value['public_ratings'],
    'release_dates': media_filters.value['release_dates'],
    'runtimes': media_filters.value['runtimes'],
    'search': media_filters.value['search'],
    'order': media_filters.value['order'],
    'content_ratings': media_filters.value['content_ratings'],
    'difficulty': media_filters.value['difficulty'],
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
        console.log('get_media', error.response)
        return []
      })

  console.log('res', result['media'].map((e)=>e.name),params)
  // console.log('res', result)

  let medias = result['media']
  search_matched_field.value = result['matched_field']

  // mark page loaded if no data returned
  if (medias.length < 1) {
    is_page_loading.value = false
    is_page_loaded.value = true
  }

  if (override) {
    media.value = medias
  } else {
    // concat result to media
    medias.forEach(entry => media.value.push(entry))
  }

  // sort tags by color
  const priority = ['gold', 'green', 'purple', 'silver', 'red']
  media.value.forEach((entry, i) => {
    media.value[i].tags.sort((a, b) => {
      const fi = priority.indexOf(a.tier)
      const si = priority.indexOf(b.tier)
      return fi - si
    })
  })

  // group media by rating
  media_grouped.value = media.value.reduce((r, e, index) => {
    if (!r[e['user_rating']]) r[e['user_rating']] = [e]
    else r[e['user_rating']].push(e)
    return r;
  }, {})

  // console.log(media_grouped.value)

  // cleanup
  is_page_loading.value = false
  page_load_status.value = 'none'
  filter_load_status.value = 'none'
  handleInfiniteScroll()

}

function handle_filter(event) {
  filter_load_status.value = 'loading'
  media_filters.value[event[0]] = event[1]
  clean_load_media()
  // console.log('event', event)
  // console.log('handle filters', media_filters.value)
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

  const endOfPage = (window.innerHeight + 600) >= container_bot.bottom;

  if (endOfPage && !is_page_loading.value && !is_page_loaded.value) {
    is_page_loading.value = true
    media_page.value += 1
    get_media()
    console.log('loading more', media_page.value)
  }

};

async function clean_load_media() {
  media_page.value = 0
  media_limit.value = 20
  is_page_loaded.value = false
  await get_media(true)
}

async function spot_reload_media() {

  const url = new URL(`${curr_api}/media/get`)
  const params = {'id': selected_media.value.id}

  const result = await axios(
      {
        method: 'POST',
        url: url,
        headers: {"Content-Type": "application/json"},
        data: JSON.stringify(params)
      })
      .then(response => response.data)
      .catch(error => {
        console.log('spot_reload_media', error.response)
        return []
      })

  if (edit_mode) console.log(result)
  media_grouped.value[result.user_rating].forEach((elem, i) => {
    if (elem.id === result.id) {
      media_grouped.value[result.user_rating][i] = result
    }
  })

}

watch(edit_pane_open, (newV, oldV) => {
  if (!newV) spot_reload_media()
})

onMounted(() => {
  page_load_status.value = 'loading'
  get_media()
  addEventListener("scroll", () => handleInfiniteScroll())
})
onUnmounted(()=>{
  removeEventListener("scroll", () => handleInfiniteScroll())
})

</script>

<template>
  <!--  <p style="position: fixed;left: 0;z-index: 1000;background-color: black">{{`is_page_loaded=${is_page_loaded}`}}</p>-->
  <!--  <p style="position: fixed;left: 0;top: 100px;z-index: 1000;background-color: black">{{`is_page_loading=${is_page_loading}`}}</p>-->

  <div class="top_feed_container" ref="feed_container" v-if="media_grouped!==undefined">

    <media-feed-filter-bar @filter="handle_filter" :load_status="filter_load_status" :media_types="media_types"
                           :tier_lists="tier_lists"
                           :matched_field="search_matched_field"
    ></media-feed-filter-bar>

    <div class="rating_box" v-for="rating in Object.keys(media_grouped).reverse()" :key="rating">

      <div class="rating_separator sticky_nav">
        <h1 style="font-weight: 500;font-size: 1em"> {{ rating }} </h1>
        <img :src="blue_star" alt="blue_star" style="width: 15px">
      </div>

      <div class="media_container_wrapper">
        <component v-for="med in media_grouped[rating]"
                   :key="med['id']"
                   :is="media_container"
                   :data="med"
                   :media_container_type_override=props.media_container_type_override
        ></component>
      </div>
    </div>

    <img v-if="page_load_status==='loading'" class="spinner" alt="spinner" :src="spinner">
    <div v-else-if="media.length < 1" class="empty_result">No result</div>

    <CreditsFooter/>


  </div>

</template>

<style scoped>
.top_feed_container {
  /*outline: 1px solid red;*/
  min-height: 100px;
  margin-top: 80px;
}

.media_container_wrapper {
  /*display: flex;*/
  /*flex-flow: row wrap;*/
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(v-bind(element_width), 0fr));
  /*grid-template-columns: repeat(5,1fr);*/
  grid-gap: 20px;
  justify-content: space-evenly;
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
  /*box-shadow: 0 0 5px #000000;*/
  box-shadow: 1px 1px 1px #000000, inset 1px 1px 0 #424052;

  border-radius: 8px;
  position: sticky;
  top: 80px;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 3px;

  transition: top 250ms;
  transition-delay: 250ms;

  -webkit-animation: fadein 0.5s; /* Safari, Chrome and Opera > 12.1 */
  -moz-animation: fadein 0.5s; /* Firefox < 16 */
  -ms-animation: fadein 0.5s; /* Internet Explorer */
  -o-animation: fadein 0.5s; /* Opera < 12.1 */
  animation: fadein 0.5s;
}

.spinner {
  margin: 75px auto auto auto;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  height: 250px;
  /*filter: opacity(75%);*/
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
    width: fit-content;
    /*padding: 7px;*/
  }
}

</style>