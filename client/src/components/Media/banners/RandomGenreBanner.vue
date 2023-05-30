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
      <MediaContainer class="movie_container" :key="mov.id" :data="mov"
                      :ratingRange="mediaRatingRanges"></MediaContainer>
    </div>
  </div>
</template>
<style scoped>
.wrapper {
  display: flex;
}
</style>