<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import gold_star from '/ui/gold_star.png'
import blue_star from '/ui/blue_star.png'
import RatingCircle from "./RatingCircle.vue";
import DifficultyGauge from "@/components/media_container/movie_container/sub_components/DifficultyGauge.vue";

let props = defineProps(["data", "max_size"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="badges_bar">

    <div class="rating_box" v-if="data['user_rating']">
      <h2 class="rating"> {{ data['user_rating'] }}</h2>
      <img :src="blue_star" alt="gold_star" class="gold_star">
    </div>

    <div class="rating_box" v-if="data['scaled_public_rating']">
      <h2 class="rating"> {{ Math.round(data['scaled_public_rating'] * 10) / 10 }}</h2>
      <img :src="gold_star" alt="gold_star" class="gold_star">
    </div>

    <div class="rating_box" v-else-if="data['public_rating']">
      <h2 class="rating"> {{ Math.round(data['public_rating'] * 10) / 10 }}</h2>
    </div>

    <rating-circle class="rating_circle" v-if="data['scaled_public_rating']>0 && data['user_rating']"
                   :text_size="max_size*1.5"
                   :score="(data['user_rating'] + data['scaled_public_rating'])/2"></rating-circle>

    <difficulty-gauge :diff="data['difficulty']"></difficulty-gauge>

  </div>
</template>

<style scoped>

.rating_circle {
  height: calc(v-bind(max_size) * 0.2px)
}

.badges_bar {
  min-height: 3px;
  min-width: 10px;
  display: flex;
  flex-flow: row nowrap;
  /*width: calc(v-bind(max_size[0]) * 1px);*/

  justify-content: flex-start;
  justify-items: center;
  align-content: center;
  align-items: center;

  gap: 5px;
}

.gold_star {
  width: calc(v-bind(max_size) * 0.07px);
  height: calc(v-bind(max_size) * 0.07px);
  /*height: 15px;*/
}

.rating_box {
  border-radius: 5px;

  box-shadow: 1px 1px 1px #000000,inset 1px 1px 0 #424052;
  background-color: #2b2a34;

  padding: 4px 5px 4px 5px;

  display: flex;
  flex-flow: row nowrap;
  text-align: center;

  align-items: center;

  gap: 2px;
}

.rating {
  /*font-size: 0.9em;*/
  font-size: calc(v-bind(max_size) * 0.005em);
  font-weight: 500;
}

</style>