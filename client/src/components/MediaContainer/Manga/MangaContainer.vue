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


</script>
<template>
  <div class="movie_container" :class="[isOpen ? 'open' : 'closed']" v-click-out-side="clickOutside" @click="isOpen = !isOpen">
    <div class="main_block">

<!--      <div class="gradient_fill"></div>-->


      <TagContainer class="tag_container" v-if="data['tags']!==undefined" :tag_input="data['tags']"></TagContainer>

      <div v-if="devMode" class="settings">
        <button @click="settingsOpen = !settingsOpen" @mousedown="emitSelectedMovie">...</button>
      </div>

      <img v-if="data['poster_path']" v-lazy="`https://uploads.mangadex.org/covers/${data['poster_path']}.256.jpg`"
           class="poster" alt="poster"
           v-click-out-side="clickOutside" @click="isOpen = !isOpen" draggable="false">


      <ContentBox class="content_box" :data="data"></ContentBox>

      <RatingBumper class="rating_bumper" v-if="data['my_rating']!==undefined" :data="data"></RatingBumper>

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

        </div>
      </div>
    </div>
  </div>
</template>
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

  visibility: hidden;
  opacity: 0;

  transition: 300ms ease-out;
}

.main_block:hover .settings {
  visibility: visible;
  opacity: 100%;
}

.tag_container {
  position: absolute;
}

.rating_bumper {
  padding: 5px;
}

.content_box {
  padding: 5px 10px 0 10px;
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

.details_wrapper {
  padding: 5px;
  overflow-y: scroll;
  overflow-wrap: break-word;
  height: 250px;
}
</style>