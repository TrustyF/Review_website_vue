<script setup>
import {inject, onMounted, watch, ref, computed, getCurrentInstance} from "vue";
import MovieContainer from '@/components/media_container/movie_container/MovieContainer.vue'
import axios from "axios";
import {log_event} from "/src/scripts/log_events.js";

let props = defineProps({
  media_types: Array,
  order: String,
  ratings: Array,
  public_ratings: Array,
  limit: {
    type: Number,
    default: 20,
  },
  tier_lists: {
    type: Array,
    default: "all",
  },
  genres: Array,
  size_override: {
    type: Array(),
    default: [500, 750],
  },
  rating_spacing: Number,
  title: String,
  defaultInView: Boolean,
});
let emits = defineEmits(["loaded"]);
const curr_api = inject("curr_api");
const session_seed = inject("session_seed");
const is_mobile = inject("is_mobile");
const rangeOfNumbers = (a, b) => [...Array(b + 1).keys()].slice(a)

let media = ref([])
let seed = ref(session_seed)
let page = ref(0)
let scroll_banner = ref()
let scroll_position = ref(0)
let scroll_elements = ref(5)

const container_height = computed(() => `${(props.size_override[1] * 0.3) + 60}px`)

async function get_media() {
  console.log('getting banner media')
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

  media.value = result.data['media']
}

async function paginate(value) {
  let children = scroll_banner.value.children
  scroll_position.value = Math.max(0, Math.min(20, scroll_position.value + (value * scroll_elements.value)))

  if (scroll_position.value === 15) {
    children[19].scrollIntoView({
      behavior: 'smooth',
      block: 'nearest',
      inline: 'end'
    })
  } else if (scroll_position.value >= 20) {
    scroll_position.value = 0
    page.value += 1
    await get_media()
    await paginate(0)
  } else {
    children[scroll_position.value].scrollIntoView({
      behavior: 'smooth',
      block: 'nearest',
      inline: 'start'
    })
  }


}

onMounted(() => {
  get_media()
  if (!props.defaultInView) log_event('anchor_in_view', 'scroll', props.title)
})

</script>

<template>
  <h1>{{ title }}</h1>
  <div class="banner_wrapper">

    <div class="nav_container">
      <div :class="`paginate ${scroll_position>1 ? 'visible':''}`" @click="paginate(-1)">
        <div class="bi-arrow-left paginate-arrow">
          <div class="arrow_gradient"/>
        </div>
      </div>
      <div class="paginate visible" @click="paginate(1)" style="transform: scaleX(-1)">
        <div class="bi-arrow-left paginate-arrow">
          <div class="arrow_gradient"/>
        </div>
      </div>
    </div>

    <div ref="scroll_banner" class="scroll_container">
      <movie-container
          v-for="med in media" :key="med.id"
          :data="med"
          :scale_mul="!is_mobile ? 0.3:0.25"
          :size_override="size_override"
          :lazy_poster="true"
      ></movie-container>
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
  pointer-events: none;
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-flow: row;
  justify-content: space-between;
  z-index: 100;
}

.paginate {
  position: relative;
  pointer-events: auto;
  z-index: 10;
  width: 6rem;
  cursor: pointer;
  height: 100%;
  display: flex;

  justify-content: center;
  align-items: center;

  opacity: 0;
  visibility: hidden;
}

.visible {
  opacity: 1;
  visibility: visible;
}

.paginate-arrow {
  /*outline: 1px solid red;*/
  font-size: 1em;
  height: 1em;
  padding: 10px;
  margin-left: -30px;
  border-radius: 10px;
  text-shadow: black 2px 2px 2px;
  display: flex;
  flex-flow: column;
  justify-content: center;
  z-index: 5;
  transition: 150ms ease-in-out;
}

.arrow_gradient {
  position: absolute;
  inset: 0;
  height: 100%;
  width: 100%;
  /*background: linear-gradient(to right, rgba(0, 0, 0, 0.5) 0%, transparent 100%);*/
  transition: 150ms ease-in-out;
  opacity: 0;
  visibility: hidden;
  z-index: -1;
}

.paginate:hover .arrow_gradient {
  transition: 100ms;
  opacity: 1;
  visibility: visible;
}

.paginate:hover .paginate-arrow {
  transition: 100ms;
  background: rgba(26, 26, 26, 0.9);
}

.scroll_container {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-flow: row;
  overflow-x: scroll;
  scroll-behavior: smooth;
  -ms-overflow-style: none; /* Internet Explorer 10+ */
  scrollbar-width: none; /* Firefox */
  gap: 20px;
}

.scroll_container::-webkit-scrollbar {
  display: none;
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