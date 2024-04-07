<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MovieContainer from '@/components/media_container/movie_container/MovieContainer.vue'
import grad_loader from "/ui/gradient_loader.webp"
import axios from "axios";

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
  limit: {
    type: Number,
    default: 20,
  },
  tier_lists: {
    type: Array,
    default: null,
  },
  genres: {
    type: Array,
    default: null,
  },
  size_override: {
    type: Array(),
    default: [500, 750],
  },
});
let emits = defineEmits(["loaded"]);
const curr_api = inject("curr_api");
const session_seed = inject("session_seed");
const is_mobile = inject("is_mobile");
const rangeOfNumbers = (a, b) => [...Array(b + 1).keys()].slice(a)

let loaded_num = ref(0)
let max_load = ref(100)
let media = ref()

const container_height = computed(() => `${(props.size_override[1] * 0.3) + 80}px`)

async function get_media() {

  const url = new URL(`${curr_api}/media/get`)
  const params = {
    'limit': props.limit,
    'page': 0,
    'types': props.media_types,
    'genres': props.genres,
    'order': props.order,
    'ratings': props.ratings,
    'content_ratings': rangeOfNumbers(20, 39).filter((elem, i) => ![33, 34].includes(elem)),
    'tier_lists': props.tier_lists,
    'session_seed': session_seed,
    'user_rating_sort_override': true,
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
  max_load.value = media.value.length
  // sort tags by color
  const priority = ['gold', 'green', 'purple', 'silver', 'red']
  media.value.forEach((entry, i) => {
    media.value[i].tags.sort((a, b) => {
      const fi = priority.indexOf(a.tier)
      const si = priority.indexOf(b.tier)
      return fi - si
    })
  })
}

// watch(loaded_num,(oldV,newV)=>{
//   if (loaded_num.value === 1) {
//     emits('loaded', true);
//   }
// })

onMounted(() => {
  get_media()
  setTimeout(() => emits('loaded', true),5)
})

</script>

<template>
  <lazy-component class="banner_wrapper">
    <div class="banner_fade"></div>
    <div class="scroll_container" v-show="loaded_num >= max_load">
      <div class="scroll_content" v-for="med in media" :key="med.id">
        <movie-container
            :data="med"
            :scale_mul="!is_mobile ? 0.3:0.25"
            :size_override="size_override"
            :lazy_poster="false"
            @is_full_loaded="loaded_num+=1"
        ></movie-container>
      </div>
    </div>
    <div class="scroll_container" v-show="loaded_num < max_load">
      <img :src="grad_loader" class="gradient_loader">
    </div>
  </lazy-component>
</template>

<style scoped>
.banner_wrapper {
  /*outline: 1px solid orange;*/
  /*border: 0.1em dotted #41404d;*/
  border-radius: 10px;
  /*padding: 15px 0 15px 15px;*/
  position: relative;
  display: flex;
  align-items: center;
  /*outline: 1px solid red;*/
  height: v-bind(container_height);
}

.scroll_container {
  position: absolute;
  width: 100%;
  height: 100%;
  /*outline: 1px solid red;*/
  overflow-x: scroll;
  /*overflow-y: hidden;*/
  display: flex;
  flex-flow: row;
  gap: 20px;
  padding: -20px 0 20px 0;
  /*white-space:nowrap;*/
  /*outline: 1px solid red;*/

  -webkit-animation: fadein 1s; /* Safari, Chrome and Opera > 12.1 */
  -moz-animation: fadein 1s; /* Firefox < 16 */
  -ms-animation: fadein 1s; /* Internet Explorer */
  -o-animation: fadein 1s; /* Opera < 12.1 */
  animation: fadein 1s;
}

::-webkit-scrollbar {
  background-color: #f5f5f5;
  border-radius: 10px;
  width: 7px;
  height: 2px;
}

::-webkit-scrollbar-thumb {
  background-color: #000000;
  border-radius: 10px;
}

.gradient_loader {
  position: absolute;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.1;
  border-radius: 10px;
}

.banner_fade {
  /*background-color: red;*/
  pointer-events: none;
  width: 100%;
  height: 100%;
  z-index: 5;
  position: absolute;
  background: linear-gradient(to right, rgba(19, 18, 21, 0) 98%, rgba(19, 18, 21, 1) 100%);
}

@media only screen and (max-width: 500px) {
  .scroll_container {
    gap: 10px;
    height: 241.1px;
  }
}

</style>