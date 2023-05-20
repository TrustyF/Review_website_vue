<script setup>
import TagContainer from "@/components/MediaContainer/Movies/components/TagContainer";
import {clickOutSide as vClickOutSide} from '@mahdikhashan/vue3-click-outside'
import RatingBumper from "@/components/MediaContainer/Movies/components/RatingBumper/RatingBumper";
import {defineProps, defineEmits, ref, onMounted, onUnmounted, watch, inject} from 'vue'
import ContentBox from "@/components/MediaContainer/Movies/components/ContentBox";

const props = defineProps(['data', 'ratingRange'])
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
  <div class="movie_container" :class="[isOpen ? 'open' : 'closed']" v-click-out-side="clickOutside"
       @click="isOpen = !isOpen">

    <div class="main_block">

      <div class="gradient_fill"></div>

      <TagContainer class="tag_container" v-if="data['tags']!==undefined" :tag_input="data['tags']"></TagContainer>

      <div v-if="devMode" class="settings">
        <button @click="settingsOpen = !settingsOpen" @mousedown="emitSelectedMovie">...</button>
      </div>

      <!--      Posters-->
      <div v-if="data['media_type']==='movie' || data['media_type']==='tv'">
        <img v-if="data['poster_path']!==undefined" v-lazy="`https://image.tmdb.org/t/p/w500${data['poster_path']}`"
             class="poster" alt="poster"
             v-click-out-side="clickOutside" @click="isOpen = !isOpen" draggable="false">
      </div>
      <div v-if="data['media_type']==='manga'">
        <img v-if="data['poster_path']" v-lazy="`https://uploads.mangadex.org/covers/${data['poster_path']}.256.jpg`"
             class="poster" alt="poster"
             v-click-out-side="clickOutside" @click="isOpen = !isOpen" draggable="false">
      </div>

      <RatingBumper class="rating_bumper" v-if="data['my_rating']!==undefined" :data="data" :range="ratingRange"></RatingBumper>

      <ContentBox class="content_box" :data="data"></ContentBox>

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
<style scoped>
.movie_container {
  /*outline: 1px solid green;*/

  background-color: white;

  width: 200px;
  min-height: 340px;
  /*max-width: 400px;*/
  /*min-width: 200px;*/

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

.content_box {
  /*outline: 1px solid red;*/
  padding: 5px 5px 5px 10px;
  /*padding: 5px;*/
}

.rating_bumper {
  position: absolute;
  transform: translate(-2px, -29px);
  /*outline: 1px solid red;*/
  padding: 0 5px 5px 5px;
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
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 90%, rgba(0, 0, 0, 0.3) 100%);
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