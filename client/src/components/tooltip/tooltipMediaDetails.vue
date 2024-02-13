<script setup>
import {inject, onMounted, watch, ref, computed, onUnmounted} from "vue";
import {useRoute} from 'vue-router';
import axios from "axios";

import gold_star from '/ui/gold_star.png'
import blue_star from '/ui/blue_star.png'
import RatingCircle from "@/components/media_container/movie_container/sub_components/RatingCircle.vue";
import BadgeTooltip from "@/components/media_container/movie_container/sub_components/badgeExpanded.vue";
import Badge from "@/components/media_container/movie_container/sub_components/badge.vue";
import external_img from '/ui/external_link.png'
import youtube_img from '/ui/youtube.png'
import diff_gauge from '/ui/circle_gauge.png'
import pen_img from '/ui/crayon.png'
import studio_img from '/ui/studio.png'
import DifficultyGauge from "@/components/media_container/movie_container/sub_components/DifficultyGauge.vue";
import spinner from '/ui/custom_spinner.webp'

// let props = defineProps({
//   id: {
//     type: Number,
//     default: null,
//   },
// });
// let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");
const media = inject("selected_media");
const media_detail_pane_open = inject("media_detail_pane_open");

const route = useRoute()
const media_id = route.params.id

const image_path = computed(() => format_image_path(media))
let image = ref()

let is_image_loaded = ref(false)

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

function handle_pane_close() {
  if (media_detail_pane_open.value) media_detail_pane_open.value = false
}

function imageHandler(event) {
  console.log(event)
  is_image_loaded.value = true
}

function format_image_path(med) {
  if (med.value['poster_path'] !== 'null' && med.value['poster_path'] !== undefined) {
    return `${curr_api}/media/get_image?path=${med.value['poster_path']}&type=${med.value['media_type']}&id=${med.value['id']}`
  } else {
    return undefined
  }
}

function handle_key_press(e) {
  if (e.keyCode === 27) handle_pane_close()
}

function open_link_new_tab(path) {
  window.open(path, '_blank');
}

function parse_diff(index) {
  if (index === undefined) return 'Accessible'
  if (index === 1) return 'Accessible'
  if (index === 2) return 'Involved'
  if (index === 3) return 'Film Snob'
  return 'Accessible'
}

onMounted(() => {
  window.addEventListener('keydown', handle_key_press)
  document.body.style.overflow = 'hidden';
})
onUnmounted(() => {
  window.removeEventListener('keydown', handle_key_press)
  document.body.style.overflow = 'scroll';
})
</script>

<template>

  <div class="media_details_wrapper" v-if="media">

    <img @click="handle_pane_close" class="close_pane_button" alt="close_edit_pane"
         src="/ui/cross_button.png">

    <div class="overflow">

      <div class="top_container">

        <img :src="image_path" @load="imageHandler" class="poster" alt="">

        <img v-if="!is_image_loaded" :src="spinner" class="spinner">

        <!--      <img v-lazy="media['poster_path']" class="bg_poster" alt="poster">-->

        <div class="footer_wrapper" v-if="is_image_loaded">

          <div class="header">
            <div>
              <h1 class="title">{{ media['name'] }}</h1>
            </div>
            <div class="secondary_info">
              <h2 class="date" v-if="media"> {{ get_year_from_release_date(media['release_date']) }}</h2>
              <h2 class="date" v-if="media['runtime']>0">•</h2>
              <h2 class="date" v-if="media['runtime']>0">{{ convert_seconds_to_time(media['runtime']) }}</h2>
              <h2 class="date" v-if="media['seasons']>0">•</h2>
              <h2 class="date" v-if="media['seasons']>0">{{ media['seasons'] + ' seasons' }} </h2>
              <h2 class="date" v-if="media['episodes']>0">•</h2>
              <h2 class="date" v-if="media['episodes']>0">{{ media['episodes'] + ' episodes' }} </h2>
              <!--            <h2 class="date" v-if="data['content_rating'] && data['content_rating'].age">•</h2>-->
              <h1 class="content_rating" v-if="media['content_rating'] && media['content_rating'].age">
                +{{ media['content_rating'].age }}</h1>
            </div>
          </div>

          <div class="badges">
            <div class="rating_box">
              <h2 class="rating"> {{ media['user_rating'] }}</h2>
              <img :src="blue_star" alt="gold_star" class="gold_star">
            </div>

            <div class="rating_box" v-if="media['scaled_public_rating']>0">
              <h2 class="rating"> {{ Math.round(media['scaled_public_rating'] * 10) / 10 }}</h2>
              <img :src="gold_star" alt="gold_star" class="gold_star">
            </div>

            <rating-circle class="rating_circle" :text_size="(350)" v-if="media['scaled_public_rating']>0"
                           :score="(media['user_rating'] + media['scaled_public_rating'])/2"></rating-circle>
          </div>

          <div v-if="media['overview']">
            <div style="display: flex;gap: 10px;align-items: center;margin-bottom: 10px">
              <h1 style="font-size: 1.2em;font-weight: 800">Overview</h1>
              <p style="font-size: 0.7em;color: grey">( Possible spoilers )</p>
            </div>
            <p class="overview" style="max-height: 100px;overflow-y: scroll">{{ media['overview'] }}</p>
          </div>

          <div style="display: flex;flex-flow:row wrap;gap: 30px">
            <div>
              <div style="display: flex;align-items: center;gap: 3px;">
                <img :src="diff_gauge" class="overview_icon">
                <p class="overview">Difficulty</p>
              </div>
              <div class="extra_info_wrapper">
                <difficulty-gauge style="margin: -10px 0 -10px -10px" :diff="media['difficulty']"></difficulty-gauge>
                <h1 style="font-size: 1em;font-weight: 800;height: fit-content">{{
                    parse_diff(media['difficulty'])
                  }}</h1>
              </div>
            </div>
            <div v-if="media['author']">
              <div style="display: flex;align-items: center;gap: 3px;">
                <img :src="pen_img" class="overview_icon">
                <p class="overview">Author</p>
              </div>
              <h1 style="font-size: 1em;font-weight: 800">{{ media['author'] }}</h1>
            </div>
            <div v-if="media['studio']">
              <div style="display: flex;align-items: center;gap: 3px;">
                <img :src="studio_img" class="overview_icon">
                <p class="overview">Studio</p>
              </div>
              <h1 style="font-size: 1em;font-weight: 800">{{ media['studio'] }}</h1>
            </div>
            <div v-if="media['external_name']!==media['name']">
              <p class="overview">Original title</p>
              <h1 style="font-size: 1em;font-weight: 800">{{ media['external_name'] }}</h1>
            </div>
          </div>

        </div>

      </div>

      <div class="bottom_container" v-if="is_image_loaded">

        <div class="genres_list" v-if="media['genres'].length > 0">
          <div class="genre_tag"
               v-for="genre in media['genres']"
               :key="genre['id']"
          >{{ genre['name'] }}
          </div>
        </div>

        <div class="tags_wrapper" v-if="media['tags']!==undefined && media['tags'].length > 0">
          <div v-for="tag in media['tags']" :key="tag['id']">
            <badge :data="tag" :min_size="200" :show_title="true"></badge>

          </div>
        </div>

        <div style="display: flex;gap: 10px">
          <div v-if="media['external_link']">
            <img v-lazy="external_img" class="button_img" @click="open_link_new_tab(media['external_link'])">
          </div>
          <div v-if="media['video_link']">
            <img v-lazy="youtube_img" class="button_img" @click="open_link_new_tab(media['video_link'])">
          </div>
        </div>


      </div>

    </div>

  </div>


</template>

<style scoped>
.media_details_wrapper {
  position: relative;
  /*outline: 1px solid red;*/
  /*min-height: 100px;*/
  height: 100%;
  /*outline: 1px solid red;*/
}

.spinner {
  position: absolute;
  inset: 0;
  margin: auto;
  height: 20%;
  object-fit: cover;

}

.extra_info_wrapper {
  display: flex;
  align-items: center;
  gap: 5px
}

.overflow {
  height: 100%;
  margin: 0 auto 0 auto;
  max-width: 1000px;
  padding: 0 40px 0 40px;
  overflow-y: scroll;
  display: flex;
  flex-flow: column;
  gap: 50px;
}

.top_container {
  /*outline: 1px solid red;*/

  height: 500px;
  width: 100%;

  position: relative;
  display: flex;
  flex-flow: row;
  justify-items: center;
  align-items: center;
}

.bottom_container {
  /*outline: 1px solid red;*/
  /*height: 500px;*/
  /*width: 100%;*/

  position: relative;
  display: flex;
  flex-flow: column;
  gap: 20px;
}

.button_img {
  height: 40px;
  filter: invert();
  border: 0.1em solid grey;
  border-radius: 10px;
  cursor: pointer;
}

.poster {
  /*outline: 1px solid purple;*/
  height: 100%;
  object-fit: contain;
  border-radius: 8px;
}

.bg_poster {
  position: absolute;
  width: 110%;
  height: 110%;
  object-fit: cover;
  z-index: -1;
  filter: opacity(20%);
  transform: translate(-5%);
}

.ratings {
  position: absolute;
  margin-left: 5px;
  left: 0;
  top: 0;
  /*transform: translate(0, v-bind(poster_size [1] + 'px')) translate(0, -50%);*/
}

.footer_wrapper {
  /*overflow-x: hidden;*/
  position: relative;
  padding: 10px 10px 10px 25px;
  display: flex;
  flex-flow: column;
  gap: 25px;
}

.header {
  display: flex;
  flex-flow: column;
  gap: 10px;
  justify-content: center;
  align-content: center;
}

.title {
  font-size: 2em;
  /*line-height: 1em;*/
  font-weight: 800;
  /*white-space: nowrap;*/
  /*text-overflow: ellipsis;*/
  /*overflow: hidden;*/
}

.content_rating {
  font-size: 1em;
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
  font-size: 1.2em;
  /*line-height: 0.7em;*/
  color: rgba(255, 255, 255, 0.5);
}

/*Genres*/
.genres_list {
  display: flex;
  flex-flow: row wrap;
  gap: 10px;
}

.genre_tag {
  padding: 7px;
  border-radius: 5px;
  font-size: 1em;
  outline: 0.15em grey solid;
}

/*Badges*/
.rating_circle {
  height: 50px;
}

.badges {
  display: flex;
  flex-flow: row nowrap;

  align-items: center;
  gap: 10px;

}

.gold_star {
  width: 15px;
  height: 15px;
}

.rating_box {
  border-radius: 5px;

  /*box-shadow: 1px 1px 1px #000000;*/
  box-shadow: 1px 1px 1px #000000, inset 1px 1px 0 #424052;

  background-color: #2b2a34;

  padding: 7px;

  display: flex;
  flex-flow: row nowrap;
  text-align: center;

  align-items: center;

  gap: 2px;
}

.rating {
  font-size: 1.2em;
  font-weight: 500;
}

.tags_wrapper {
  display: flex;
  flex-flow: row wrap;
  gap: 10px;
}

.overview {
  color: lightgrey;
  font-size: 0.9em;
  line-height: 1.2em;
  height: fit-content;
}

.overview_icon {
  height: 30px;
  filter: invert();
}

.close_pane_button {
  cursor: pointer;
  position: absolute;
  filter: invert();
  right: 20px;
  top: 20px;
  width: 30px;
  padding: 30px;
  margin: -30px;
  object-fit: contain;
  z-index: 10;
}

@media only screen and (max-width: 500px) {
  .overflow {
    gap: 0;
    margin: 0;
    /*max-width: initial;*/
    padding: 0;
  }

  .top_container {
    flex-flow: column;
    height: auto;
  }

  .bottom_container {
    padding: 25px;
  }

  .footer_wrapper {
    padding: 25px;
  }

  .poster {
    margin-left: 25px;
    height: 300px;
    margin-right: auto;
  }

  .close_pane_button {
    /*outline: 1px solid red;*/
    right: 0;
    top: 0;
    width: 20px;
    padding: 30px;
    margin: -30px;
  }
}
</style>