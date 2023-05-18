<script setup>
import TagContainer from "@/components/MediaContainer/Movies/components/TagContainer";
import {clickOutSide as vClickOutSide} from '@mahdikhashan/vue3-click-outside'
import RatingBumper from "@/components/MediaContainer/Manga/components/RatingBumper";
import {defineProps, defineEmits, ref, onMounted, onUnmounted, watch, inject} from 'vue'
import ContentBox from "@/components/MediaContainer/Movies/components/ContentBox";

const props = defineProps(['data'])
const emits = defineEmits(['MovieEdit'])

const devMode = inject('devMode')

let isOpen = ref(false)
const isSeen = ref(false)
const outOfFocus = ref(false)
const settingsOpen = ref(false)

let tagAmount = ref(0)

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

function calcTagAmount(){
  if (props.data['tags'] !== undefined) {
    tagAmount.value = props.data['tags'].length
  }
}

calcTagAmount()

</script>
<template>
  <div class="movie_container" :class="[isOpen ? 'open' : 'closed']">
    <div class="main_block">

      <div class="gradient_fill"></div>
      <div class="tag_gradient_wrapper">
        <div :class="'tag_gradient_background' + [tagAmount===1 ? ' one_tag' : ''] + [tagAmount===2 ? ' two_tag' : ''] + [tagAmount===3 ? ' three_tag' : '']"></div>
      </div>

      <RatingBumper class="rating_bumper" v-if="data['my_rating']!==undefined" :data="data"></RatingBumper>

      <TagContainer class="tag_container" v-if="data['tags']!==undefined" :tag_input="data['tags']"></TagContainer>

      <div v-if="devMode" class="settings">
        <button @click="settingsOpen = !settingsOpen" @mousedown="emitSelectedMovie">...</button>
      </div>

      <img v-if="data['poster_path']" v-lazy="`https://uploads.mangadex.org/covers/${data['poster_path']}.256.jpg`"
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

  /*overflow: hidden;*/
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

.gradient_fill {
  width: 200px;
  position: absolute;
  height: 300px;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 85%, rgba(0, 0, 0, 0.5) 100%);
  /*border-radius: 8px;*/
  pointer-events: none;
}

.tag_gradient_wrapper {
  position: absolute;
  width: 200px;
  height: 300px;
  overflow: hidden;
  border-radius: 8px 0 0 0;
  pointer-events: none;
  /*outline: green solid 1px;*/
}

.tag_gradient_background {
  /*outline: green solid 1px;*/
  overflow: hidden;
  width: 100px;
  position: absolute;
  transform: translate(-70%, -15%);
  background-color: rgba(0, 0, 0, 0.9);
  filter: blur(20px);
}
.one_tag {
  height: 50px;
  }
.two_tag {
  height: 130px;
}
.three_tag {
  height: 190px;
}

.gold_glow {
  box-shadow: 0 0 8px rgb(0, 0, 0), 0 0 16px rgb(255, 204, 109);
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