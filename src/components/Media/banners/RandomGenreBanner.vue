<script setup>
import MediaContainer from '@/components/Media/MediaContainer'
import {inject, watch, defineProps} from 'vue'
import axios from 'axios'
import {ref, onMounted, toRefs} from 'vue'

const props = defineProps(['mediaType'])
const current_api = inject('curr_api')

let bannerMedia = ref({})
const mediaRatingRanges = ref({})

function get_rating_range() {
  axios.post(`${current_api}/media/get_rating_range`, {
    'media_type': props['mediaType']
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
  })
      .then(response => {
        bannerMedia.value = response.data
        console.log(bannerMedia)
      })
}

onMounted(() => {
  get_rating_range()
})
</script>
<template>
  <div class="wrapper">
    <div v-for="mov in bannerMedia" :key="mov.title">
      <h1 class="genre_title hover_box dark_accent">{{mov['genres'][0]}}</h1>
      <MediaContainer class="movie_container" :key="mov.id" :data="mov"
                      :ratingRange="mediaRatingRanges"></MediaContainer>
    </div>
  </div>
</template>
<style scoped>
.wrapper {
  /*outline: 1px red solid;*/
  display: flex;
  justify-content: space-between;
}
.genre_title {
  font-size: 0.9em;
  font-weight: normal;
}
.hover_box {
  margin-bottom: 10px;
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
  transform: translate(0,15px);
  left: 0;
  right: 0;
  margin: 10px auto;
  width: 0;
  height: 0;
  border-top: 7px solid #2b2a34;
  border-left: 7px solid transparent;
  border-right: 7px solid transparent;
}

</style>