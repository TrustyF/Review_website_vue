<script setup>
import MediaContainer from '@/components/Media/MediaContainer'
import {inject, watch, defineProps} from 'vue'
import {ref, onMounted, onUnmounted, toRefs} from 'vue'
import {eventThrottle} from "@/utils";

const props = defineProps(['bannerMedia', 'bannerType', 'mediaType', 'bannerIndex', 'bannerFit'])
const input = toRefs(props)

// let bannerMedia =  input['bannerMedia'].value
// let bannerIndex =  input['bannerIndex'].value

let mediaRanges = inject('mediaRanges')
let page = ref(0)

// let startIndex = bannerLength * page.value

let slicedBanner = ref([])

const arrow_left = './assets/ui/arrow_left_single_white.png'
const arrow_right = './assets/ui/arrow_right_single_white.png'

function format_header(movie) {
  let genres = movie['genres']

  if (genres.length > 1) {
    return genres[0] + ' / ' + genres[1]
  } else {
    return genres[0]
  }
}

function page_forward() {
  console.log(props['bannerFit']*5,page.value)
  if (page.value !== (props['bannerFit']*5)-props['bannerFit']){
    page.value += props['bannerFit']
  }
}

function page_backwards() {
  if (page.value !== 0){
    page.value -= props['bannerFit']
  }
}

</script>
<template>
  <div class="bg_wrapper">
    <div class="genre_wrapper" id="genre_box">

        <div v-for="mov in bannerMedia[bannerIndex].slice(0+page,bannerFit+page)" :key="mov.title"
             class="banner_wrapper">

          <div class="hover_box dark_accent">
            <h1 class="genre_title">{{ format_header(mov) }}</h1>
          </div>

          <MediaContainer id="media_container" :key="mov.id" :data="mov"
                          :ratingRange="mediaRanges[mediaType]"
                          :media-type="mediaType"
          ></MediaContainer>
        </div>

    </div>
    <div class="button_wrapper right" @click="page_forward">
      <img :src="arrow_left" alt="refresh_selection" class="refresh_button">
    </div>
    <div class="button_wrapper left" @click="page_backwards">
      <img :src="arrow_right" alt="refresh_selection" class="refresh_button">
    </div>
  </div>

</template>
<style scoped>

.bg_wrapper {
  min-height: 400px;
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
  cursor: pointer;
  position: absolute;
  /*transform: translate(-400%, 0);*/
  top: 45%;
  width: 20px;
  height: 20px;
  background-color: #2b2a34;
  padding: 10px;
  border-radius: 100%;
  transition: 50ms ease-in-out;
}

.left {
  left: 6%;
}

.right {
  right: 6%;

}

.button_wrapper:hover {
  background-color: #41404d;
}

.refresh_button {
  width: 100%;
  height: 100%;
  user-select: none;
  -webkit-user-drag: none;
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