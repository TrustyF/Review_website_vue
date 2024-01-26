<script setup>
import {inject, onMounted, watch, ref, computed, provide} from "vue";
import gold_star from '@/assets/ui/gold_star.png'
import blue_star from '@/assets/ui/blue_star.png'
import RatingCircle from "@/components/media_container/movie_container/sub_components/RatingCircle.vue";
import BadgeTooltip from "@/components/media_container/movie_container/sub_components/badgeExpanded.vue";
import Badge from "@/components/media_container/movie_container/sub_components/badge.vue";

const image_path = computed(() => `${curr_api}/media/get_image?path=${props.data['poster_path']}&id=${props.data['id']}`)
let props = defineProps(["data", "container_scale", "container_size"]);
let emits = defineEmits(["media_data"]);
const curr_api = inject("curr_api");

const poster_size = computed(() => [
  props['container_size'][0] * props['container_scale'],
  props['container_size'][1] * props['container_scale']
])
const min_size = computed(() => Math.min(poster_size.value[0], poster_size.value[1]))

function convert_seconds_to_time(f_seconds) {
  let minutes = f_seconds % 60
  let hours = (f_seconds - minutes) / 60

  if (hours > 0){
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

</script>

<template>
  <div class="movie_mobile_container_wrapper">

    <div class="poster_wrapper">
      <img @click="open_link_new_tab(data['external_link'])" class="poster" alt="poster" v-lazy="image_path"/>
      <div class="poster_gradient"></div>

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

    </div>

    <div class="footer_wrapper">

      <div class="header">
        <div class="title">{{ data['name'] }}</div>
        <div class="secondary_info">
          <h2 class="date" v-if="data['release_date']!==undefined"> {{
              get_year_from_release_date(data['release_date'])
            }}</h2>
          <h2 class="date" v-if="data['runtime']>0">{{ ' • ' + convert_seconds_to_time(data['runtime']) }}</h2>
          <h2 class="date" v-if="data['seasons']>0">{{ ' • ' + data['seasons'] + ' seasons' }} </h2>
          <h2 class="date" v-if="data['episodes']>0">{{ ' • ' + data['episodes'] + ' episodes' }} </h2>
        </div>
      </div>

      <div class="genres_list" v-if="data['genres'].length > 0">
        <div class="genre_tag"
             v-for="genre in data['genres']"
             :key="genre['id']"
        >{{ genre['name'] }}
        </div>
      </div>


      <div class="tags_wrapper" v-if="data['tags']!==undefined && data['tags']!==null">
        <div v-for="tag in data['tags']" :key="tag['id']">
          <!--          <badge-tooltip class="tag" :data="tag" :text_size="0.6"></badge-tooltip>-->
          <badge :data="tag" :min_size="150" :show_title="true"></badge>

        </div>
      </div>

    </div>


  </div>
</template>

<style scoped>
.movie_mobile_container_wrapper {
  cursor: pointer;
  display: flex;
  flex-flow: row nowrap;
  justify-items: center;
  align-items: center;
  border-radius: 8px;

  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);
  background-color: #25222a;
  padding: 5px;
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

  border-radius: 8px;
  object-fit: cover;
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
  padding: 10px 10px 10px 15px;
  display: flex;
  flex-flow: column nowrap;
  gap: 7px;
}

.header {
  display: flex;
  flex-flow: column;
  /*gap: 2px;*/
}

.title {
  font-size: 1.2em;
  line-height: normal;
  font-weight: 500;
}

.secondary_info {
  display: flex;
  gap: 3px;
}

.date {
  margin-top: 5px;
  font-size: 0.7em;
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
  /*background: white;*/
  /*color: black;*/
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
  position: absolute;
  /*height: 20px;*/

  align-items: center;
  gap: 5px;

  bottom: 5px;
  left: 8px;
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

  box-shadow: 1px 1px 1px #000000;
  background-color: #2b2a34;

  padding: 3px;

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
  flex-flow: row wrap;
  gap: 10px;
}

.tag {
  /*height: calc(v-bind(min_size) * 0.3px);*/
  position: relative;
  opacity: 100%;
  visibility: visible;
}
</style>