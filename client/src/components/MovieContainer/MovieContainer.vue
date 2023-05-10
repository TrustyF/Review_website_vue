<script setup>
import TagContainer from "@/components/MovieContainer/components/TagContainer";
import {clickOutSide as vClickOutSide} from '@mahdikhashan/vue3-click-outside'
import RatingBumper from "@/components/MovieContainer/components/RatingBumper";
import {defineProps, defineEmits, ref, onMounted,onUnmounted, watch, inject} from 'vue'
import ContentBox from "@/components/MovieContainer/components/ContentBox";

const props = defineProps(['data'])
const emits = defineEmits(['MovieEdit'])

const devMode = inject('devMode')

let isOpen = ref(false)
const isSeen = ref(false)
const outOfFocus = ref(false)
const settingsOpen = ref(false)

const screenRect = ref(null)
const screenSide = ref(false)

function timeConvert(n) {
  const hours = (n / 60);
  const rhours = Math.floor(hours);
  const minutes = (hours - rhours) * 60;
  const rminutes = Math.round(minutes);
  return rhours + " h " + rminutes + " minutes";
}

function clickOutside(input) {
  isOpen.value = false
}

function emitSelectedMovie(input) {
  emits('MovieEdit', props['data'])
}

function calcScreenSide() {
  let rect = screenRect.value.getBoundingClientRect()
  let screen = [window.outerWidth, window.outerHeight]

  screenSide.value = rect.right > (screen[0] / 2);
}

onMounted(() => {
  calcScreenSide()
  window.addEventListener('resize', calcScreenSide)
})

onUnmounted(()=>{
  window.removeEventListener('resize', calcScreenSide)
})

</script>
<template>
  <div ref="screenRect" class="movie_container" :class="[isOpen ? 'open' : 'closed'] + [isSeen ? ' seen' : '']">
    <div class="main_block">

      <RatingBumper class="rating_bumper" v-if="data['my_rating']!==undefined" :data="data"></RatingBumper>

      <TagContainer class="tag_container" v-if="data['tags']!==undefined" :tag_input="data['tags']"
                    :screen_side="screenSide"></TagContainer>

      <div v-if="devMode" class="settings">
        <button @click="settingsOpen = !settingsOpen" @mousedown="emitSelectedMovie">...</button>
      </div>

      <img v-if="data['poster_path']!==undefined" v-lazy="`https://image.tmdb.org/t/p/w500${data['poster_path']}`"
           class="poster" alt="poster"
           v-click-out-side="clickOutside" @click="isOpen = !isOpen" draggable="false">

      <ContentBox :data="data"></ContentBox>

    </div>

    <div class="expanded">
      <div class="overview">

        <h3 class="heading">Overview</h3>
        <div class="details_wrapper">
          <p class="rank" v-if="data['overview']" style="margin-bottom:5px;">
            {{ data['overview'] }}
          </p>

          <h3 class="heading">Extras</h3>
          <p class="rank" v-if="data['genres']" style="margin-bottom:5px;">
            {{ data['genres'].map(elem => elem).join(', ') }}
          </p>
          <p class="rank" style="margin-bottom:5px;" v-if="data['runtime'] && data['media_type']==='movie'">
            {{ "Duration: " + timeConvert(data['runtime']) }}
          </p>
          <a :href="data['imdb_url']" target="_blank" rel="noopener noreferrer">
            <button type="button"
                    style="background-color: #F5C518;border-radius: 3px;padding: 3px;outline: 1px black solid;border-style: none;cursor:pointer ">
              Imdb
            </button>
          </a>
        </div>
      </div>
    </div>

    <!--    <div class="seen_block_cover">-->

    <!--    </div>-->
    <!--    <div class="seen_checkbox_wrapper">-->
    <!--      <div class="seen_checkbox_hitBox" @mousedown="isSeen = !isSeen">-->
    <!--        <div class="seen_checkbox_box">-->
    <!--          <div :class="'checkmark' + [isSeen ? '' : ' seen' ]"></div>-->
    <!--        </div>-->
    <!--      </div>-->
    <!--    </div>-->
  </div>
</template>
<script>
export default {
  name: "MovieContainer"
}
</script>
<style scoped>
.movie_container {
  /*outline: 1px solid green;*/

  background-color: white;

  width: 200px;
  min-height: 340px;
  /*max-width: 400px;*/
  /*min-width: 200px;*/

  margin: 15px;
  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);

  overflow: hidden;
  transition: 0.2s ease;

  display: flex;

}

.settings {
  position: absolute;
  transform: translate(173px, 3px);
}

.tag_container {
  position: absolute;
}

.rating_bumper {
  position: absolute;
  transform: translate(3px, 277px);
}

.seen_checkbox_wrapper {
  /*outline: red 1px solid;*/
  position: absolute;
  /*margin-left: 0px;*/
  margin-top: 335px;
}

.seen_checkbox_box {
  user-select: none;
  position: absolute;
  top: 58%;
  left: 89%;
  /*transform: translate(0%, -50%);*/
  width: 15px;
  height: 15px;
  /*border: 2px solid black;*/
  box-shadow: 0 0 2px 1px rgba(0, 0, 0, 0.35);
  background-color: white;
  border-radius: 3px;
  transition: 0.2s ease;
  opacity: 0;
}

.seen .seen_checkbox_box {
  background-color: royalblue;
  border-color: royalblue;
  box-shadow: 0 0 3px 0 rgba(0, 0, 0, 0.5);
  opacity: 1;
}

.seen_checkbox_hitBox:hover .seen_checkbox_box {
  opacity: 1;
}

.seen_checkbox_hitBox {
  /*outline: 1px purple solid;*/
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(0%, -67%);
  cursor: pointer;
  width: 200px;
  height: 53px;
}

.seen .checkmark {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) translate(0, -1px) rotate(45deg);
  display: inline-block;
  /*margin-left: 60%;*/
  height: 7px;
  width: 3px;
  border-bottom: 2px solid white;
  border-right: 2px solid white;
}

.main_block {
  /*outline: 2px solid purple;*/
  width: 200px;
  display: block;
}

.expanded {
  /*outline: 1px red solid;*/
  border-radius: 8px 8px 0 0;

  position: absolute;
  width: 200px;
  height: 300px;

  background-color: rgba(255, 255, 255, 0.9);

  font-size: 0.65em;
  text-align: left;

  visibility: hidden;
  opacity: 0;
  transition: all 0.1s;
}

.open .expanded {
  visibility: visible;
  opacity: 1;
}

.overview {
  padding: 10px;
}

.seen_block_cover {
  border-radius: 8px;
  /*outline: 1px red solid;*/

  padding: 20px 20px 20px 20px;
  position: absolute;

  width: 160px;
  height: 313px;

  background-color: rgba(255, 255, 255, 0.85);

  visibility: hidden;
  opacity: 0;
  transition: all 0.5s;
}

.seen .seen_block_cover {
  visibility: visible;
  opacity: 1;
}

.heading {
  /*padding: 10px 0 5px 0 ;*/
  line-height: 25px;
  text-decoration: underline;
}

.poster {
  cursor: help;
  user-select: none;
  border-radius: 8px 8px 0 0;
  width: 200px;
  aspect-ratio: 1/1.5;
}

.poster::after {
  background-image: linear-gradient(to bottom, rgba(255, 255, 0, 0) 0%, rgba(0, 0, 0, 1) 100%);
}


.open .tags_list_poster {
  opacity: 0;
  visibility: hidden;
}

.editor_button {
  position: absolute;
  transform: translate(174px, 2px);
}
</style>