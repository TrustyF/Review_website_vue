<script setup>
import MediaContainer from '@/components/Media/MediaContainer'
import {inject, watch, defineProps} from 'vue'
import axios from 'axios'
import {ref, onMounted, onUnmounted, toRefs} from 'vue'
import {eventThrottle} from "@/utils";

let sessionSeed = inject('sessionSeed')
let mediaRanges = inject('mediaRanges')

const rewind = './assets/ui/rewind.png'

const props = defineProps(['bannerType', 'mediaType'])
const input = toRefs(props)
const current_api = inject('curr_api')

let bannerMedia = ref({})
let num_media_fit = ref(0)

function get_recent_releases() {
  axios.post(`${current_api}/media/get_recent_release`, {
    'media_type': props['mediaType'],
    'max_media': num_media_fit.value,
    'session_seed': sessionSeed
  })
      .then(response => {
        bannerMedia.value = response.data
        // console.log(bannerMedia)
      })
}

function get_random_genre() {
  axios.post(`${current_api}/media/get_rand_genre`, {
    'media_type': props['mediaType'],
    'max_media': num_media_fit.value,
    'session_seed': sessionSeed
  })
      .then(response => {
        bannerMedia.value = response.data
        // console.log(bannerMedia)
      })
}

function update_media() {
  if (input['bannerType'].value === 'random_genre') {
    get_random_genre()
  }
  if (input['bannerType'].value === 'recent_release') {
    get_recent_releases()
  }
}

function format_header(movie) {
  let genres = movie['genres']

  if (genres.length > 1) {
    return genres[0] + ' / ' + genres[1]
  } else {
    return genres[0]
  }
}

function calc_screen_fit() {

  let w_box = document.getElementById("genre_box").getBoundingClientRect()
  let gap = 20
  let media_width = 200
  let fit_num = Math.floor(w_box.width / (media_width + (gap)))

  if (num_media_fit.value !== fit_num) {
    num_media_fit.value = fit_num
    // console.log(num_media_fit.value)
    update_media()
  }

}

function refresh() {
  sessionSeed = Math.random()
  update_media()
}

onMounted(() => {
  calc_screen_fit()
  addEventListener('resize', eventThrottle(calc_screen_fit, 100))
})
onUnmounted(() => {
  removeEventListener('resize', calc_screen_fit)
})

</script>
<template>
  <div class="bg_wrapper">
    <div class="genre_wrapper" id="genre_box">

      <div v-for="mov in bannerMedia" :key="mov.title" class="banner_wrapper">

        <div class="hover_box dark_accent">
          <h1 class="genre_title">{{ format_header(mov) }}</h1>
        </div>

        <MediaContainer id="media_container" :key="mov.id" :data="mov"
                        :ratingRange="mediaRanges[mediaType]"></MediaContainer>
      </div>

    </div>
    <div class="button_wrapper" @click="refresh" v-show="bannerType==='random_genre'">
      <img :src="rewind" alt="refresh_selection" class="refresh_button">
    </div>
  </div>

</template>
<style scoped>

.bg_wrapper {
  /*outline: 1px red solid;*/
  display: flex;
  position: relative;
  background-color: #1c1b23;
  padding: 40px;
  flex-flow: column;
  gap: 20px;
}

.genre_wrapper {
  /*outline: 1px red solid;*/
  width: 80%;
  margin: auto;
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

#media_container {
  /*outline: 1px red solid;*/
}

.button_wrapper {
  position: absolute;
  /*transform: translate(-400%, 0);*/
  right: 8%;
  width: 20px;
  height: 20px;
  background-color: #2b2a34;
  padding: 10px;
  border-radius: 100%;
  transition: 50ms ease-in-out;
}

.button_wrapper:hover {
  background-color: #41404d;
}

.refresh_button {
  width: 100%;
  height: 100%;
}

.banner_wrapper {
  /*outline: 1px solid blue;*/
  width: 200px;
}

.genre_title {
  /*width: 200px;*/
  /*outline: 1px solid red;*/
  font-size: 0.8em;
  font-weight: lighter;
  text-align: center;
  white-space: nowrap;
  text-overflow: "-";
  overflow: hidden;
}

.hover_box {
  /*width: 200px;*/
  margin-bottom: 20px;
  border-radius: 5px;
  filter: drop-shadow(0px 0 2px rgba(0, 0, 0, 0.5));
  padding: 10px;
  /*outline: 2px red solid;*/
}

.hover_box:after {
  content: '';
  position: absolute;
  display: inline-block;
  left: 50%;
  top: 100%;
  transform: translate(-50%, 0);

  border-top: 7px solid #2b2a34;
  /*border-top: 7px solid red;*/
  border-left: 7px solid transparent;
  border-right: 7px solid transparent;
}

</style>