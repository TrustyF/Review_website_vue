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

let media = ref(new Array(20).fill().map((e, i) => {
  return {
    name: 'none',
    release_date: 'none',
  }
}))

async function get_media() {

  const url = new URL(`${curr_api}/media/get`)
  const params = {
    'limit': 20,
    'page': 0,
    'type': props['media_type'],
    'ratings': [7, 10],
    'session_seed': session_seed,
    'user_rating_sort_override': true,
  }

  let result = await axios(
      {
        method: 'POST',
        url:url,
        headers: {"Content-Type": "application/json"},
        data: JSON.stringify(params)
      })
      .catch(error => {
        console.log('media_scroll_banner_get_media', error.response)
        return []
      })

  console.log(result)
  if (result.status !== 200) return

  media.value = result.data

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
    <div class="scroll_container" v-if="media.length > 0">
      <div class="scroll_content" v-for="med in media" :key="med.id">
        <movie-container
            :data="med"
            :lazy_poster="false"
            :scale_mul="!is_mobile ? 0.3:0.2"
            :size_override="[500,750]"
        ></movie-container>
      </div>
      <div class="scroll_content" v-for="med in media" :key="med.id">
        <movie-container
            :data="med"
            :lazy_poster="false"
            :scale_mul="!is_mobile ? 0.3:0.2"
            :size_override="[500,750]"
        ></movie-container>
      </div>
    </div>
    <div class="scroll_container" v-else>
      <img class="spinner" alt="spinner" :src="spinner">
    </div>
  </div>
</template>

<style scoped>
.banner_wrapper {
  /*outline: 1px solid red;*/
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;

  height: calc(750 * 0.4px);
  width: 100%;
}

.scroll_container {
  position: relative;
  overflow-x: hidden;
  height: 100%;
  width: 100%;

  display: flex;
  flex-flow: row;
  gap: 20px;
  justify-content: center;
  align-items: center;
  /*outline: 1px solid red;*/
}
.spinner {
  position: relative;
  height: 50%;
  /*object-fit: cover;*/
  /*margin: 0 auto 0 auto;*/
}

.scroll_content {
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
  background: linear-gradient(to right, rgba(19, 18, 21, 0) 95%, rgba(19, 18, 21, 1) 100%), linear-gradient(to left, rgba(19, 18, 21, 0) 95%, rgba(19, 18, 21, 1) 100%);
}

@keyframes scroll_banner {
  to {
    transform: translate(calc(-2000% - 800px));
  }
}
</style>