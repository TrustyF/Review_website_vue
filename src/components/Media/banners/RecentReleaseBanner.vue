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
  axios.post(`${current_api}/media/get_recent_release`, {
    'media_type': props['mediaType'],
    'max_media': props['max_media']
  })
      .then(response => {
        bannerMedia.value = response.data
        console.log(bannerMedia)
      })
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
    <div class="wrapper">
      <div v-for="mov in bannerMedia" :key="mov.title">
        <!--      <h1 class="genre_title hover_box dark_accent">{{ mov['genres'][0] }}</h1>-->
        <MediaContainer class="movie_container" :key="mov.id" :data="mov"
                        :ratingRange="mediaRatingRanges"></MediaContainer>
      </div>
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

.wrapper {
  /*outline: 1px red solid;*/
  display: flex;
  justify-content: space-between;
  gap: 25px;
  width: 80%;
  margin: auto;
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
  transform: translate(0, 15px);
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