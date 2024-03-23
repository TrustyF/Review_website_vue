<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MovieContainer from '@/components/media_container/movie_container/MovieContainer.vue'
import axios from "axios";

let props = defineProps({
  media_type: {
    type: String,
    default: null,
  }
});
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");
const session_seed = inject("session_seed");
const is_mobile = inject("is_mobile");
let med_limit = 30
const rangeOfNumbers = (a, b) => [...Array(b + 1).keys()].slice(a)

let media = ref(new Array(med_limit).fill().map((e, i) => {
  return {
    name: '',
    release_date: '',
  }
}))

async function get_media() {
  console.log("2. attempt to get scroll banner media")


  const url = new URL(`${curr_api}/media/get`)
  const params = {
    'limit': med_limit,
    'page': 0,
    'types': ['movie', 'tv', 'manga', 'game'],
    'ratings': [5, 10],
    'content_ratings': rangeOfNumbers(20, 39).filter((elem, i) => ![33, 34].includes(elem)),
    'session_seed': session_seed,
    'user_rating_sort_override': true,
  }

  let result = await axios(
      {
        method: 'POST',
        url: url,
        headers: {"Content-Type": "application/json"},
        // signal: AbortSignal.timeout(2000),
        data: JSON.stringify(params)
      })

  media.value = result.data['media']

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

onMounted(() => {
  console.log("1. mounted media scroll banner")
  get_media()
})

</script>

<template>
  <div class="banner_wrapper">
    <div class="banner_fade"></div>

    <div class="scroll_content">
      <img style="object-fit: contain;height: 100%;" :src="`${curr_api}/media/get_scroll_banner`">
      <img style="object-fit: contain;height: 100%;" :src="`${curr_api}/media/get_scroll_banner`">
    </div>

  </div>
</template>

<style scoped>
.banner_wrapper {
  position: absolute;
  z-index: -5;
  left: 0;
  right: 0;
  /*height: 170%;*/
  height: 300px;
  filter: opacity(50%);
  /*outline: 5px greenyellow solid;*/
  overflow-x: hidden;
}

.scroll_content {
  display: flex;
  height: 100%;
  width: fit-content;
  animation: scroll_banner 150s linear infinite;
  will-change: transform;
}

.banner_fade {
  /*background-color: red;*/
  pointer-events: none;
  width: 100%;
  height: 100%;
  z-index: 5;
  position: absolute;
  background: linear-gradient(to right, rgba(19, 18, 21, 0) 80%, rgba(19, 18, 21, 1) 100%),
  linear-gradient(to left, rgba(19, 18, 21, 0) 80%, rgba(19, 18, 21, 1) 100%),
  linear-gradient(to top, rgba(19, 18, 21, 0) 50%, rgba(19, 18, 21, 1) 95%),
  linear-gradient(to bottom, rgba(19, 18, 21, 0) 50%, rgba(19, 18, 21, 1) 95%);
}

@media only screen and (max-width: 500px) {
  /*.banner_wrapper {*/
  /*  margin-top: 1px;*/
  /*}*/
  .scroll_content {
    animation: scroll_banner 150s linear infinite;
  }
}

@keyframes scroll_banner {
  to {
    transform: translate(calc(-50%));
  }
}
</style>