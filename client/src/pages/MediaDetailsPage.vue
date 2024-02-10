<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import {useRoute} from 'vue-router';
import axios from "axios";

import gold_star from '/ui/gold_star.png'
import blue_star from '/ui/blue_star.png'
import RatingCircle from "@/components/media_container/movie_container/sub_components/RatingCircle.vue";
import BadgeTooltip from "@/components/media_container/movie_container/sub_components/badgeExpanded.vue";
import Badge from "@/components/media_container/movie_container/sub_components/badge.vue";

// let props = defineProps({
//   id: {
//     type: Number,
//     default: null,
//   },
// });
// let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

const route = useRoute()
const media_id = route.params.id

let is_image_loaded = ref(false)

const media = ref()

async function get_media() {

  const url = new URL(`${curr_api}/media/get`)
  const params = {
    'id': media_id
  }

  const result = await axios(
      {
        method: 'POST',
        url: url,
        headers: {"Content-Type": "application/json"},
        data: JSON.stringify(params)
      })
      .then(response => response.data)
      .catch(error => {
        console.log('get_media', error.response)
        return []
      })

  console.log('res', result)

  // sort tags by color
  const priority = ['gold', 'green', 'purple', 'silver', 'red']

  result.tags.sort((a, b) => {
    const fi = priority.indexOf(a.tier)
    const si = priority.indexOf(b.tier)
    return fi - si
  })

  media.value = result
}

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

onMounted(() => {
  get_media()
})
</script>

<template>
  <div class="media_details_wrapper" v-if="media">

    <div class="top_container">

      <img v-lazy="media['poster_path']" @load="is_image_loaded=true" class="poster" alt="poster">

      <!--      <img v-lazy="media['poster_path']" class="bg_poster" alt="poster">-->

      <div class="footer_wrapper" v-if="is_image_loaded">

        <div class="header">
          <div>
            <h1 class="title">{{ media['name'] }}</h1>
          </div>
          <div class="secondary_info">
            <h2 class="date" v-if="media"> {{
                get_year_from_release_date(media['release_date'])
              }}</h2>
            <h2 class="date" v-if="media['runtime']>0">{{ ' • ' + convert_seconds_to_time(media['runtime']) }}</h2>
            <h2 class="date" v-if="media['seasons']>0">{{ ' • ' + media['seasons'] + ' seasons' }} </h2>
            <h2 class="date" v-if="media['episodes']>0">{{ ' • ' + media['episodes'] + ' episodes' }} </h2>
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

        <div v-if="media['overview']" style="max-height: 100px;overflow-y: scroll">
          <h1 style="font-size: 1.2em;font-weight: 800;margin-bottom: 10px">Overview</h1>
          <p class="overview">{{ media['overview'] }}</p>
        </div>

        <div style="display: flex;gap: 30px">
          <div v-if="media['author']">
            <p class="overview">Author</p>
            <h1 style="font-size: 1em;font-weight: 800">{{ media['author'] }}</h1>
          </div>
          <div v-if="media['studio']">
            <p class="overview">Studio</p>
            <h1 style="font-size: 1em;font-weight: 800">{{ media['studio'] }}</h1>
          </div>
        </div>

      </div>

    </div>

    <div class="bottom_container">

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

    </div>

  </div>
</template>

<style scoped>
.media_details_wrapper {
  /*outline: 1px solid red;*/
  min-height: 100px;
  margin-top: 80px;
  /*outline: 1px solid red;*/
  display: flex;
  flex-flow: column;
  gap: 50px;
}

.top_container {
  height: 500px;
  width: 100%;

  position: relative;
  display: flex;
  flex-flow: row;
  justify-items: center;
  align-items: center;
}

.bottom_container {
  /*height: 500px;*/
  width: 100%;

  position: relative;
  display: flex;
  flex-flow: column;
  gap: 10px;
  /*justify-items: center;*/
  /*align-items: center;*/
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
  overflow-x: hidden;
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
  flex-flow: row;
  gap: 10px;
}

.overview {
  font-size: 0.9em;
  line-height: 1.2em;
}

@media only screen and (max-width: 500px) {
  .media_details_wrapper {
    outline: 1px solid greenyellow;
  }
}
</style>