<script setup>
import {inject, onMounted, watch, ref, computed, provide} from "vue";
import gold_star from '@/assets/ui/gold_star.png'
import blue_star from '@/assets/ui/blue_star.png'
import RatingCircle from "@/components/MediaContainer/MediaHelperComponents/RatingCircle.vue";

let props = defineProps(["data", "container_scale", "container_size"]);
let emits = defineEmits(["media_data"]);
const curr_api = inject("curr_api");

const poster_size = computed(() => [
  props['container_size'][0] * props['container_scale'],
  props['container_size'][1] * props['container_scale']
])

function convert_seconds_to_time(f_seconds) {
  let minutes = f_seconds % 60
  let hours = (f_seconds - minutes) / 60
  return hours + 'h ' + minutes + 'm';
}

</script>

<template>
  <div class="movie_container_wrapper" @click="emits('media_data',data)">

    <img class="poster" alt="poster" v-lazy="`${curr_api}/media/get_image?id=${data['id']}`"/>

    <div class="footer_wrapper">

      <div class="header">
        <div class="title">{{ data['name'] }}</div>
        <div class="secondary_info">
          <h2 class="date">{{ data['release_date'].substring(0, 4) }}</h2>
          <h2 class="date" v-if="data['runtime']>0">{{ ' • ' + convert_seconds_to_time(data['runtime']) }}</h2>
          <h2 class="date" v-if="data['seasons']>0">{{ ' • ' + data['seasons'] + ' seasons' }} </h2>
          <h2 class="date" v-if="data['episodes']>0">{{ ' • ' + data['episodes'] + ' episodes' }} </h2>
        </div>
      </div>

      <div class="genres_list" v-if="data['genres']">
        <div class="genre_tag"
             v-for="genre in data['genres']"
             :key="genre['id']"
        >{{ genre['name'] }}
        </div>
      </div>

      <div class="badges">
        <div class="rating_box">
          <h2 class="rating"> {{ data['user_rating'] }}</h2>
          <img :src="blue_star" alt="gold_star" class="gold_star">
        </div>

        <div class="rating_box">
          <h2 class="rating"> {{ Math.round(data['scaled_public_rating'] * 10) / 10 }}</h2>
          <img :src="gold_star" alt="gold_star" class="gold_star">
        </div>

        <rating-circle class="rating_circle" :text_size="0.7"
                       :score="(data['user_rating'] + data['scaled_public_rating'])/2"></rating-circle>
      </div>

    </div>


  </div>
</template>

<style scoped>
.movie_container_wrapper {
  display: flex;
  flex-flow: row nowrap;
  justify-items: center;
  align-items: center;
  border-radius: 8px;
}

.poster {
  width: v-bind(poster_size [0] + 'px');
  height: v-bind(poster_size [1] + 'px');
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);

  border-radius: 8px;
  object-fit: cover;
}

/* Footer*/
.footer_wrapper {
  padding: 0 0 0 20px;
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
  height: 30px;
}

.badges {
  display: flex;
  flex-flow: row wrap;

  justify-content: flex-start;
  align-items: center;
  gap: 5px;
}

.gold_star {
  width: 10px;
  height: 10px;
}

.rating_box {
  border-radius: 5px;

  box-shadow: 1px 1px 1px #000000;
  background-color: #2b2a34;

  padding: 5px;

  display: flex;
  flex-flow: row nowrap;
  text-align: center;

  align-items: center;

  gap: 2px;
}

.rating {
  font-size: 0.8em;
  height: 0.85em;
  font-weight: 500;
}
</style>