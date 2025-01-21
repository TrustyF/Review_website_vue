<script setup>
import {inject, onMounted, ref, computed} from "vue";
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
    default: ()=>["all"],
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

  function countElementsInView(children) {
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    const viewportWidth = window.innerWidth || document.documentElement.clientWidth;

    return Array.from(children).filter(child => {
      const rect = child.getBoundingClientRect();
      const parent = child.parentElement;

      // Check if the element is within the viewport
      const isWithinViewport =
          rect.top >= 0 &&
          rect.left >= 0 &&
          rect.bottom <= viewportHeight &&
          rect.right <= viewportWidth;

      if (!isWithinViewport) return false;

      // Check if the element is within its parent's bounds (handling overflow hidden)
      if (parent) {
        const parentRect = parent.getBoundingClientRect();
        const isWithinParentBounds =
            rect.top >= parentRect.top &&
            rect.left >= parentRect.left &&
            rect.bottom <= parentRect.bottom &&
            rect.right <= parentRect.right;

        return isWithinParentBounds;
      }

      return true;
    }).length;
  }

  let children = scroll_banner.value.children
  let scroll_amount = 5

  scroll_amount = countElementsInView(children)
  console.log(countElementsInView(children))


  scroll_position.value = Math.max(0, Math.min(20, scroll_position.value + (value * scroll_amount)))

  log_event('paginate banner', 'int', `${props['title']} ${scroll_position.value}-${page.value}`)

  if (scroll_position.value === 15) {
    children[20].scrollIntoView({
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
      <div class="paginate">
        <div class="bi-arrow-left-short paginate-arrow">
          <div class="paginate-arrow-hitbox" @click="paginate(-1)"/>
        </div>
      </div>
      <div class="paginate" style="transform: scaleX(-1)">
        <div class="bi-arrow-left-short paginate-arrow">
          <div class="paginate-arrow-hitbox" @click="paginate(1)"/>
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
  z-index: 10;
  height: 100%;
  display: flex;

  justify-content: flex-start;
  align-items: center;

  transition: 100ms;
  opacity: 0;
  visibility: hidden;
  transform: translate(5px);
}

.paginate-arrow {
  position: relative;
  font-size: 1.5em;
  /*-webkit-text-stroke: 1px white;*/
  height: fit-content;
  padding: 7px 2px 7px 2px;
  margin: 3px;
  text-shadow: black 1px 1px 3px;
  display: flex;
  flex-flow: column;
  justify-content: center;
  z-index: 5;
  border-radius: 10px;
  transition: 200ms;
}

.paginate-arrow-hitbox {
  position: absolute;
  left: 50%;
  transform: translate(-50%, 10%);
  border-radius: 10px;
  width: 100%;
  height: 100%;
  padding: 10px 15px 25px 15px;
  cursor: pointer;
  pointer-events: auto;
}

.banner_wrapper:hover .paginate {
  transform: translate(0px);
  transition: 100ms;
  opacity: 1;
  visibility: visible;
}

.paginate-arrow:hover {
  background-color: rgba(29, 27, 36, 1);
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