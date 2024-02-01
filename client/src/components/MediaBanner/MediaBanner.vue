<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MovieContainer from '@/components/media_container/movie_container/MovieContainer.vue'

let props = defineProps(["media_type"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");
const session_seed = inject("session_seed");

let media = ref([...Array(10).keys()])

async function get_media() {

  const url = new URL(`${curr_api}/media/get`)
  const params = {
    'limit': 20,
    'page': 0,
    'type': props['media_type'],
    // 'ratings': [5, 10],
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
}

onMounted(() => {
  get_media()
})

</script>

<template>
  <div class="banner_wrapper">
    <div class="banner_fade"></div>
    <div class="scroll_container" id="home_scroll_container">
      <div class="scroll_content" style="user-select: none;" v-for="med in media" :key="med.id">
        <movie-container
            :data="med"
            :lazy_poster="false"
            :container_size="[500,750]"
            :container_scale="0.25"
        ></movie-container>
      </div>
      <div class="scroll_content" style="user-select: none;" v-for="med in media" :key="med.id">
        <movie-container
            :data="med"
            :lazy_poster="false"
            :container_size="[500,750]"
            :container_scale="0.25"
        ></movie-container>
      </div>
    </div>
  </div>
</template>

<style scoped>
.banner_wrapper {
  position: relative;
  height: 250px;
  /*background-color: #1c1b23;*/
  display: flex;
  align-items: center;
}

.scroll_container {
  /*position: relative;*/
  overflow-x: hidden;
  display: flex;
  flex-flow: row;
  gap: 10px;
  /*outline: 1px solid red;*/
}

.scroll_content {
  animation: scroll_banner 100s linear infinite;
  will-change: transform;
}

.banner_fade {
  /*background-color: red;*/
  width: 100%;
  height: 100%;
  z-index: 5;
  position: absolute;
  background: linear-gradient(to right, rgba(19, 18, 21, 0) 95%, rgba(19, 18, 21, 1) 100%), linear-gradient(to left, rgba(19, 18, 21, 0) 95%, rgba(19, 18, 21, 1) 100%);
}

@keyframes scroll_banner {
  to {
    transform: translate(calc(-2000% - 200px));
  }
}
</style>