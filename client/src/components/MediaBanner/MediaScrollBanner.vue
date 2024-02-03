<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MovieContainer from '@/components/media_container/movie_container/MovieContainer.vue'

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

  media.value = await fetch(url,
      {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(params)
      })
      .then(response => {
        console.log('response', response)
        return response.json()
      })

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
    <div class="scroll_container">
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
  </div>
</template>

<style scoped>
.banner_wrapper {
  /*outline: 1px solid red;*/
  position: relative;
  display: flex;
  align-items: center;
}

.scroll_container {
  /*position: relative;*/
  overflow-x: hidden;
  display: flex;
  flex-flow: row;
  gap: 20px;
  /*outline: 1px solid red;*/
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