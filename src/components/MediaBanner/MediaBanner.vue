<script setup>
import {inject, onMounted, watch, ref, computed, getCurrentInstance} from "vue";
import MovieContainer from '@/components/media_container/movie_container/MovieContainer.vue'
import axios from "axios";
import {log_event} from "/src/scripts/log_events.js";

let props = defineProps({
  media_types: {
    type: Array,
    default: null,
  },
  order: {
    type: String,
    default: null,
  },
  ratings: {
    type: Array,
    default: null,
  },
  public_ratings: {
    type: Array,
    default: null,
  },
  limit: {
    type: Number,
    default: 5,
  },
  tier_lists: {
    type: Array,
    default: "all",
  },
  genres: {
    type: Array,
    default: null,
  },
  size_override: {
    type: Array(),
    default: [500, 750],
  },
  rating_spacing: {
    type: Number,
    default: null,
  },
  title: {
    type: String,
    default: null,
  },
  defaultInView: {
    type: Boolean,
    default: false,
  },
});
let emits = defineEmits(["loaded"]);
const curr_api = inject("curr_api");
const session_seed = inject("session_seed");
const is_mobile = inject("is_mobile");
const rangeOfNumbers = (a, b) => [...Array(b + 1).keys()].slice(a)

let media = ref([])
let seed = ref(session_seed)
let page = ref(0)

const container_height = computed(() => `${(props.size_override[1] * 0.3) + 60}px`)

async function get_media() {
  // console.log('getting banner media')
  const url = new URL(`${curr_api}/media/get`)
  const params = {
    'limit': props.limit,
    'page': page.value,
    'types': props.media_types,
    'genres': props.genres,
    'order': props.order,
    'ratings': props.ratings,
    'public_ratings': props.public_ratings,
    'content_ratings': rangeOfNumbers(20, 39).filter((elem, i) => ![33, 34].includes(elem)),
    'tier_lists': props.tier_lists,
    'session_seed': seed.value,
    'user_rating_sort_override': true,
    'rating_spacing': props.rating_spacing,
  }

  let result = await axios(
      {
        method: 'POST',
        url: url,
        // signal: AbortSignal.timeout(2000),
        // timeout:2000,
        headers: {"Content-Type": "application/json"},
        data: JSON.stringify(params)
      })

  return result.data['media']
}

async function paginate(value){
  page.value += value
  page.value = Math.max(page.value,0)

  media.value = await get_media()
}


onMounted(() => {
  paginate(0)
  if (!props.defaultInView) log_event('anchor_in_view', 'scroll', props.title)
})

</script>

<template>
  <h1>{{ title }}</h1>
  <div class="banner_wrapper">

    <div class="nav_container">
      <div class="paginate">
        <div class="arrow_gradient"></div>
        <div @click="paginate(-1)" class="bi-arrow-left paginate-arrow" v-show="!is_mobile"/>
      </div>
      <div class="paginate">
        <div class="arrow_gradient" style="transform: rotate(180deg)"></div>
        <div @click="paginate(1)" class="bi-arrow-right paginate-arrow" v-show="!is_mobile"/>
      </div>
    </div>

    <div class="scroll_container">
      <div class="scroll_content" v-for="med in media" :key="med.id">
        <movie-container
            :data="med"
            :scale_mul="!is_mobile ? 0.3:0.25"
            :size_override="size_override"
            :lazy_poster="true"
        ></movie-container>
      </div>
    </div>

  </div>
</template>

<style scoped>
h1 {
  margin: 0 0 20px 0
}

.banner_wrapper {
  position: relative;
  height: v-bind(container_height);
}
.nav_container {
  position: absolute;
  width: 100%;
  height: 100%;
  outline: 1px solid red;
  display: flex;
  flex-flow: row;
  justify-content: space-between;
  z-index: 100;
}
.paginate {
  /*border: 1px solid blue;*/
  z-index: 10;
  width: 4rem;
  cursor: pointer;
  height: 100%;
  display: flex;
}

.paginate-arrow {
  text-align: center;
  font-size: 1em;
  padding: 10px;
  display: flex;
  flex-flow: column;
  justify-content: center;
  z-index: 10;
}
.arrow_gradient {
  position: absolute;
  height: 100%;
  width: 4rem;
  background: linear-gradient(to right, rgba(0, 0, 0, 0.8), transparent);
  transition: 250ms ease-in-out;
  opacity: 0;
  visibility: hidden;
}
.paginate:hover .arrow_gradient{
  transition: 100ms;
  opacity: 1;
  visibility: visible;
}
.scroll_container {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-flow: row;
  /*align-items: center;*/
  /*justify-content: space-between;*/
  gap: 20px;
}

.scroll_content {
  -webkit-animation: fadein 1s; /* Safari, Chrome and Opera > 12.1 */
  -moz-animation: fadein 1s; /* Firefox < 16 */
  -ms-animation: fadein 1s; /* Internet Explorer */
  -o-animation: fadein 1s; /* Opera < 12.1 */
  animation: fadein 1s;
}


@media only screen and (max-width: 500px) {
  .scroll_container {
    gap: 10px;
    /*height: 250px;*/
  }

  .banner_wrapper {
    height: calc(v-bind(container_height) * 0.85);
  }
}

</style>