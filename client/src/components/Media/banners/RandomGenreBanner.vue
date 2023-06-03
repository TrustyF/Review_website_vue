<script setup>
import MediaContainer from '@/components/Media/MediaContainer'
import {inject, watch, defineProps} from 'vue'
import axios from 'axios'
import {ref, onMounted, toRefs} from 'vue'

const rewind = './assets/ui/rewind.png'

const props = defineProps(['mediaType', 'max_media'])
const input = toRefs(props)
const current_api = inject('curr_api')

let bannerMedia = ref({})
const mediaRatingRanges = ref({})

function get_rating_range() {
  axios.post(`${current_api}/media/get_rating_range`, {
    'media_type': input['mediaType'].value
  })
      .then(response => {
        if (response.status === 200) {
          console.log('ranges', response.status, response.data)
          mediaRatingRanges.value = response.data
          get_movies()
        }
      })
}

function get_movies() {
  console.log('updating banner')
  axios.post(`${current_api}/media/get_rand_genre`, {
    'media_type': props['mediaType'],
    'max_media': props['max_media']
  })
      .then(response => {
        bannerMedia.value = response.data
        console.log(bannerMedia)
      })
}

function format_header(movie) {
  let genres = movie['genres']

  if (genres.length > 1) {
    return genres[0] + ' / ' + genres[1]
  } else {
    return genres[0]
  }
}

onMounted(() => {
  get_rating_range()
})

watch(input['max_media'], (newV, oldV) => {
  console.log('props updated')
  get_movies()
})
</script>
<template>
  <div class="bg_wrapper">
    <div class="genre_wrapper">
      <div v-for="mov in bannerMedia" :key="mov.title">
        <h1 class="genre_title hover_box dark_accent">{{ format_header(mov) }}</h1>
        <MediaContainer class="movie_container" :key="mov.id" :data="mov"
                        :ratingRange="mediaRatingRanges"></MediaContainer>
      </div>
    </div>
    <div class="button_wrapper" @click="get_movies">
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
  /*border-radius: 15px;*/
  flex-flow: column;
  gap: 20px;
}

.genre_wrapper {
  /*outline: 1px red solid;*/
  width: 80%;
  margin: auto;
  display: flex;
  justify-content: space-between;
  gap: 25px;
  z-index: 10;
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

.genre_title {
  font-size: 0.8em;
  font-weight: lighter;
}

.hover_box {
  margin-bottom: 20px;
  font-weight: normal;
  /*color: black;*/
  /*background-color: white;*/
  padding: 10px;
  border-radius: 5px;
  filter: drop-shadow(0px 0 2px rgba(0, 0, 0, 0.5));
  text-align: center;
  /*outline: 2px red solid;*/
}

.hover_box:after {
  content: '';
  position: absolute;
  display: inline-block;
  transform: translate(0, 190%);
  left: 0;
  right: 0;
  width: 0;
  height: 0;
  margin: 10px auto;
  border-top: 7px solid #2b2a34;
  border-left: 7px solid transparent;
  border-right: 7px solid transparent;
}

</style>