<script setup>
import TagContainer from "@/components/Media/components/TagContainer";
import {clickOutSide as vClickOutSide} from '@mahdikhashan/vue3-click-outside'
import RatingBumper from "@/components/Media/components/RatingBumper/RatingBumper";
import {defineProps, defineEmits, ref, toRefs, onMounted, onUnmounted, watch, inject} from 'vue'
import ContentBox from "@/components/Media/components/ContentBox";

const props = defineProps(['data', 'rating_desc', 'mediaType'])
const input = toRefs(props)
const emits = defineEmits(['MovieEdit', 'MovieUpdate'])

const devMode = inject('devMode')
const forceVis = inject('forceVis')
const current_api = inject('curr_api')

let isOpen = ref(false)
const isSeen = ref(false)
const outOfFocus = ref(false)
const settingsOpen = ref(false)

let main_block_hover = ref(false)

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

function RatingChange(state) {

  const url = new URL(`${current_api}/media/update`)
  let newRating = Number(input['data'].value['my_rating'])
  // console.log(newRating, state)

  if (state) {
    newRating += 1
  } else {
    newRating -= 1
  }

  input['data'].value['my_rating'] = String(newRating)

  const params = {
    'data': input['data'].value,
    'media_type': input['mediaType'].value
  }

  fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(params)
  })

      // Handle http error
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        }
        emits('MovieUpdate')
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

function build_cover_request(info) {
  let data = input.data.value
  let media_type = input['mediaType'].value

  return `${current_api}/media/cover?poster_path=${encodeURIComponent(data['poster_path'])}&type=${media_type}`
}

watch(forceVis, () => {
  // console.log('movie', forceVis.value)
  main_block_hover.value = forceVis.value
})

</script>
<template>
  <div class="movie_container" :class="isOpen ? 'open ' : 'closed '"
       v-click-out-side="clickOutside"
       @click="isOpen = !isOpen">

<!--    <div v-if="data.hasOwnProperty('tags') && data['tags']!==undefined && data['tags']!==null">-->
<!--      <div v-if="data['tags'].length > 0">-->
<!--        <div class="fill" v-if="Object.values(data['tags'][0]).includes('Childhood')"></div>-->
<!--      </div>-->
<!--    </div>-->

    <div class="main_block" @mouseover="main_block_hover = true" @mouseleave="main_block_hover = false">

      <TagContainer :class="forceVis ? 'tag_container  vis_override':'tag_container'" v-if="data['tags']!==null"
                    :tag_input="data['tags']"></TagContainer>

      <div v-if="devMode" class="settings">
        <button style="width: 35px;height: 35px" @click="settingsOpen = !settingsOpen" @mousedown="emitSelectedMovie">
          ...
        </button>

        <button style="width: 35px;height: 35px" @mousedown="RatingChange(true)">
          ▲
        </button>
        <button style="width: 35px;height: 35px" @mousedown="RatingChange(false)">
          ▼
        </button>
      </div>

      <img v-if="mediaType==='movie'||mediaType==='tv'||mediaType==='anime'"
           v-lazy="`https://image.tmdb.org/t/p/w500${data['poster_path']}`"
           class="poster" alt="poster" draggable="false">

      <img v-if="mediaType==='manga'"
           v-lazy="build_cover_request()"
           class="poster" alt="poster" draggable="false">

      <img v-if="mediaType==='game'"
           v-lazy="data['poster_path']"
           class="game_poster" alt="poster" draggable="false">

      <RatingBumper class="rating_bumper" v-if="data['my_rating']!==undefined" :data="data"
                    :rating_desc="rating_desc" :hover="main_block_hover" :mediaType="mediaType"></RatingBumper>

      <ContentBox class="content_box" :data="data"></ContentBox>

    </div>

    <div class="expanded">
      <div class="overview">

        <h3 class="heading">Overview</h3>
        <div class="details_wrapper">
          <p class="rank" v-if="data['overview']" style="margin-bottom:5px; line-height: 120%">
            {{ data['overview'] }}
          </p>

          <h3 class="heading">Extras</h3>
          <p class="rank" v-if="data['genres']" style="margin-bottom:5px;">
            {{ data['genres'].map(elem => elem).join(', ') }}
          </p>

          <div v-if="data['media_type']==='movie' || data['media_type']==='tv' || data['media_type']==='anime'">
            <p class="rank" style="margin-bottom:5px;" v-if="data['runtime'] && data['media_type']==='movie'">
              {{ "Duration: " + timeConvert(data['runtime']) }}
            </p>
            <a :href="`https://www.imdb.com/title/${data['imdb_id']}/`" target="_blank" rel="noopener noreferrer">
              <button type="button"
                      style="background-color: #F5C518;border-radius: 3px;padding: 3px;outline: 1px black solid;border-style: none;cursor:pointer ">
                Imdb
              </button>
            </a>
            <p>{{data['imdb_url']}}</p>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>
<style scoped>
.movie_container {
  /*outline: 1px solid green;*/

  width: 200px;
  /*height: 350px;*/
  /*height: fit-content;*/
  position: relative;
  color: white;

  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);

  background-color: #2b2a34;

  /*overflow: hidden;*/
  transition: 0.2s ease;

  display: flex;
}

.poster {
  object-fit: cover;
  cursor: help;
  user-select: none;
  border-radius: 8px 8px 0 0;
  /*width: 200px;*/

  width: 100%;
  height: 310px;
}

.game_poster {
  object-fit: cover;
  object-position: top;
  cursor: help;
  user-select: none;
  border-radius: 8px 8px 0 0;
  width: 200px;

  /*width: 100%;*/
  height: 267px;
}

.settings {
  position: absolute;
  transform: translate(180px, 3px);
  display: flex;
  flex-flow: column wrap;
  gap: 10px;

  visibility: hidden;
  opacity: 0;

  transition: 50ms ease-in-out;
  z-index: 999;
}

.main_block:hover .settings {
  transform: translate(162px, 3px);
  visibility: visible;
  opacity: 100%;
}

.tag_container {
  position: absolute;
  transform: translate(-7px, 0);

  /*outline: 1px solid blue;*/
  visibility: hidden;
  opacity: 0;
  transition: 50ms ease-in-out;
  transition-delay: 50ms;

}

.main_block:hover .tag_container {
  transform: translate(0, 0);
  visibility: visible;
  opacity: 100%;
  transition-delay: 0ms;
}

.vis_override {
  transform: translate(0, 0);
  visibility: visible;
  opacity: 100%;
}


.content_box {
  /*outline: 1px solid red;*/
  /*padding: 5px;*/
}

.rating_bumper {
  position: absolute;
  transform: translate(-2px, -35px);
  padding: 5px;
  /*transform: translate(-2px, -15px);*/
  /*outline: 1px solid red;*/
  /*padding: 0 5px 5px 5px;*/

  /*visibility: hidden;*/
  /*opacity: 0;*/

  /*transition: 50ms ease-in-out;*/
  /*transition-delay: 50ms;*/
}

.main_block {
  width: 200px;
  display: block;
}

.expanded {
  /*outline: 1px red solid;*/
  border-radius: 8px;

  position: absolute;
  width: 200px;
  height: 100%;

  background-color: rgba(0, 0, 0, 0.9);

  font-size: 0.7em;
  text-align: left;

  visibility: hidden;
  opacity: 0;
  transition: all 0.1s;
}

.dark .expanded {
  background-color: rgba(20, 20, 20, 0.9);

}

.open .expanded {
  visibility: visible;
  opacity: 1;
}

.overview {
  padding: 10px;
  width: 190px;
  overflow: hidden;
}

.heading {
  /*padding: 10px 0 5px 0 ;*/
  line-height: 25px;
  text-decoration: underline;
  font-size: 1.2em;
  font-weight: bold;
}

.fill {
  top: 0;
  left: 0;
  width: 200px;
  height: 100%;
  position: absolute;
  background-color: rgba(19, 18, 21, 0.5);
  border-radius: 7px;
  pointer-events: none;
  z-index: 900;
  transition: 50ms ease-in-out;
}

.movie_container:hover .fill {
  background-color: rgba(0, 0, 0, 0);
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
  width: 100%;
  height: 250px;
  padding: 5px 25px 5px 5px;
  overflow-y: scroll;
  overflow-wrap: break-word;
}
</style>