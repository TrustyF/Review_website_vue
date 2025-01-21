<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
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

let img_loads = ref(0)

let media = ref(new Array(med_limit).fill().map((e, i) => {
  return {
    name: '',
    release_date: '',
  }
}))

async function get_media() {

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
  get_media()
})

</script>

<template>
  <div class="banner_wrapper">
    <div class="banner_fade"></div>
    <img class="banner_img fade_anim" v-show="img_loads>=1" @load="img_loads+=1"
         :src="`${curr_api}/media/get_scroll_banner`">
  </div>
</template>

<style scoped>
.banner_wrapper {
  z-index: -1;
  position: absolute;

  left: 50%;
  top: 60px;

  transform: translate(-50%);

  width: 100vw;
  height: 300px;
  overflow-x: hidden;
  opacity: 0.25;
}
.banner_img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  /*filter: blur(5px);*/
}

.banner_fade {
  /*background-color: red;*/
  pointer-events: none;
  width: 100%;
  height: 100%;
  z-index: 5;
  position: absolute;
  background:
  linear-gradient(to bottom, transparent 60%, rgba(19, 18, 21, 1) 100%);
}

.fade_anim {
  height: 100%;
}

@media only screen and (max-width: 500px) {
}
</style>