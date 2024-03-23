<script setup>
import {inject, onMounted, watch, ref, computed, provide} from "vue";
import gold_star from '/ui/gold_star.png'
import blue_star from '/ui/blue_star.png'
import RatingCircle from "@/components/media_container/movie_container/sub_components/RatingCircle.vue";
import BadgeTooltip from "@/components/media_container/movie_container/sub_components/badgeExpanded.vue";
import Badge from "@/components/media_container/movie_container/sub_components/badge.vue";
import {useRouter} from 'vue-router'

import external_img from '/ui/external_link.png'
import youtube_img from '/ui/youtube.png'
import DifficultyGauge from "./sub_components/DifficultyGauge.vue";

const image_path = computed(() => `${curr_api}/media/get_image?path=${props.data['poster_path']}&id=${props.data['id']}`)
let props = defineProps(["data", "container_scale", "container_size"]);
let emits = defineEmits(["media_data"]);

const curr_api = inject("curr_api");
let media_scales = inject('media_scales')
let vis_container_content_rating = inject('vis_container_content_rating')
let selected_media = inject('selected_media')
const media_detail_pane_open = inject("media_detail_pane_open");

const router = useRouter()


const media_type = computed(() => props['data']['media_type'])

const poster_size = computed(() => [
  media_scales.value[media_type.value]['size'][0] * media_scales.value[media_type.value]['scale'],
  media_scales.value[media_type.value]['size'][1] * media_scales.value[media_type.value]['scale']
])
const min_size = computed(() => Math.min(poster_size.value[0], poster_size.value[1]))

function convert_seconds_to_time(f_seconds) {
  let minutes = f_seconds % 60
  let hours = (f_seconds - minutes) / 60

  if (hours > 0) {
    return hours + 'h ' + minutes + 'm';
  } else {
    return minutes + 'm';
  }
}

function get_year_from_release_date(string) {

  if (typeof string === 'string') {
    return string.substring(0, 4)
  } else {
    return undefined
  }
}

function open_link_new_tab(path) {
  window.open(path, '_blank');
}

function push_to_details() {
  selected_media.value = props['data']
  media_detail_pane_open.value = true
}
</script>

<template>
  <div class="movie_mobile_container_wrapper">

    <div class="poster_wrapper">
      <img @click="push_to_details" class="poster" alt="poster" v-lazy="image_path" lazy="loading"/>
      <!--      <div class="poster_gradient"></div>-->
    </div>

    <div class="footer_wrapper">

      <div class="header">
        <div>
          <h1 class="title">{{ data['name'] }}</h1>
        </div>
        <div class="secondary_info">
          <h2 class="date" v-if="data['release_date']!==undefined"> {{
              get_year_from_release_date(data['release_date'])
            }}</h2>
          <h2 class="date" v-if="data['runtime']>0">{{ ' • ' + convert_seconds_to_time(data['runtime']) }}</h2>
          <h2 class="date" v-if="data['seasons']>0">{{ ' • ' + data['seasons'] + ' seasons' }} </h2>
          <h2 class="date" v-if="data['episodes']>0">{{ ' • ' + data['episodes'] + ' episodes' }} </h2>
          <!--            <h2 class="date" v-if="data['content_rating'] && data['content_rating'].age">•</h2>-->
          <h1 class="content_rating" v-if="data['content_rating'] && data['content_rating'].age">
            +{{ data['content_rating'].age }}</h1>
        </div>
      </div>

      <div class="badges">
        <div class="rating_box">
          <h2 class="rating"> {{ data['user_rating'] }}</h2>
          <img :src="blue_star" alt="gold_star" class="gold_star">
        </div>

        <div class="rating_box" v-if="data['scaled_public_rating']>0">
          <h2 class="rating"> {{ Math.round(data['scaled_public_rating'] * 10) / 10 }}</h2>
          <img :src="gold_star" alt="gold_star" class="gold_star">
        </div>

        <rating-circle class="rating_circle" :text_size="(150)" v-if="data['scaled_public_rating']>0"
                       :score="(data['user_rating'] + data['scaled_public_rating'])/2"></rating-circle>
      </div>

      <div class="genres_list" v-if="data['genres'].length > 0">
        <div class="genre_tag"
             v-for="genre in data['genres']"
             :key="genre['id']"
        >{{ genre['name'] }}
        </div>
      </div>

      <div class="tags_wrapper" v-if="data['tags']!==undefined && data['tags'].length > 0">
        <div v-for="tag in data['tags']" :key="tag['id']">
          <!--          <badge-tooltip class="tag" :data="tag" :text_size="0.6"></badge-tooltip>-->
          <badge :data="tag" :min_size="150"></badge>

        </div>
      </div>


    </div>

<!--    <div class="edit_tools_wrapper">-->
<!--      <img v-if="data['video_link']" class="edit_tool" title="go to video" :src="youtube_img"-->
<!--           @click="open_link_new_tab(data['video_link'])">-->
<!--      <img v-if="data['external_link']" class="edit_tool" title="go to external website" :src="external_img"-->
<!--           @click="open_link_new_tab(data['external_link'])">-->
<!--    </div>-->

    <difficulty-gauge class="diff" :diff="data['difficulty']"></difficulty-gauge>

  </div>
</template>

<style scoped>
.movie_mobile_container_wrapper {
  /*outline: 1px solid red;*/
  position: relative;
  display: flex;
  flex-flow: row;
  justify-items: center;
  align-items: center;
  border-radius: 8px;

  /*box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);*/
  background-color: #25222a;
  padding: 5px;

  user-select: none;
  /*outline: 1px solid red;*/
  -webkit-animation: fadein 0.5s; /* Safari, Chrome and Opera > 12.1 */
  -moz-animation: fadein 0.5s; /* Firefox < 16 */
  -ms-animation: fadein 0.5s; /* Internet Explorer */
  -o-animation: fadein 0.5s; /* Opera < 12.1 */
  animation: fadein 0.5s;
}

.poster_wrapper {
  position: relative;
  display: flex;
  flex-flow: column nowrap;
  align-items: flex-start;
  /*margin-bottom: auto;*/
}

.poster {
  position: relative;
  width: v-bind(poster_size [0] + 'px');
  height: v-bind(poster_size [1] + 'px');
  box-shadow: 1px 1px 7px rgba(0, 0, 0, 0.5);

  border-radius: 8px;
  object-fit: scale-down;
  transition: opacity 0.5s;
}

.poster[lazy=loading] {
  opacity: 0;
}
.diff {
  position: absolute;
  bottom: 0;
  right: 0;
  margin: 10px;
}
.poster_gradient {
  content: "";
  pointer-events: none;
  position: absolute;
  border-radius: 8px;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 90%, rgba(0, 0, 0, 0.5) 100%);
  left: 0;
  top: 0;
  width: v-bind(poster_size [0] + 'px');
  height: v-bind(poster_size [1] + 'px');
}

/* Footer*/
.footer_wrapper {
  overflow-x: hidden;
  position: relative;
  padding: 10px 10px 10px 15px;
  display: flex;
  flex-flow: column;
  gap: 10px;
}

.header {
  display: flex;
  flex-flow: column;
  gap: 5px;
  justify-content: center;
  align-content: center;
}

.title {
  font-size: 1em;
  /*line-height: 1em;*/
  font-weight: 500;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

.content_rating {
  font-size: 0.7em;
  /*line-height: 0.7em;*/
  font-weight: 300;
  padding: 2px 5px 2px 4px;
  border-radius: 7px;
  color: grey;
  border: 0.1em dimgrey solid;
}

.secondary_info {
  display: flex;
  flex-flow: row;
  gap: 5px;
  align-items: center;
}

.date {
  font-size: 0.7em;
  /*line-height: 0.7em;*/
  color: rgba(255, 255, 255, 0.5);
}

/*Genres*/
.genres_list {
  display: flex;
  flex-flow: row wrap;
  gap: 5px;
}

.genre_tag {
  padding: 5px;
  border-radius: 5px;
  font-size: 0.7em;
  outline: 0.1em grey solid;
}

/*Badges*/
.rating_circle {
  height: 20px;
}

.badges {
  display: flex;
  flex-flow: row nowrap;
  /*position: absolute;*/
  /*height: 20px;*/

  align-items: center;
  gap: 5px;

  bottom: 5px;
  left: 5px;
  /*transform: translate(0, -50%);*/
  /*margin-bottom: -15px;*/
  /*margin-left: 5px;*/
}

.gold_star {
  width: 10px;
  height: 10px;
}

.rating_box {
  border-radius: 5px;

  /*box-shadow: 1px 1px 1px #000000;*/
  box-shadow: 1px 1px 1px #000000, inset 1px 1px 0 #424052;

  background-color: #2b2a34;

  padding: 4px;

  display: flex;
  flex-flow: row nowrap;
  text-align: center;

  align-items: center;

  gap: 2px;
}

.rating {
  font-size: 0.6em;
  font-weight: 500;
}

.tags_wrapper {
  display: flex;
  flex-flow: row;
  gap: 10px;

  /*box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);*/
  /*background-color: #25222a;*/
  /*padding: 7px 0 7px 5px;*/
}

.edit_tools_wrapper {
  pointer-events: none;

  z-index: 100;
  /*width: v-bind(poster_size [0] + 'px');*/
  position: absolute;
  padding-bottom: 5px;

  display: flex;
  flex-flow: column;
  /*gap: 5px;*/

  align-items: center;

  left: 0;
  bottom: 0;

}

.edit_tool {
  border: unset;
  /*margin: 5px;*/
  padding: 5px;
  pointer-events: auto;
  cursor: pointer;

  width: calc(v-bind(min_size) * 0.015em);
  height: calc(v-bind(min_size) * 0.015em);

  /*background-color: #d8dbd3;*/
  /*box-shadow: 1px 1px 1px white, inset 1px 1px 0 #bdc0bb;*/

  filter: invert() drop-shadow(0.07em 0 0.01em black) drop-shadow(0 0.07em 0.01em black) drop-shadow(-0.07em 0 0.01em black) drop-shadow(0 -0.07em 0.01em black);
  border-radius: 5px;
}

.tag {
  /*height: calc(v-bind(min_size) * 0.3px);*/
  position: relative;
  opacity: 100%;
  visibility: visible;
}
</style>