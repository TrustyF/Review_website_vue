<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import gold_star from '@/assets/ui/gold_star.png'
import blue_star from '@/assets/ui/blue_star.png'
import RatingCircle from "@/components/MediaContainer/MediaHelperComponents/RatingCircle.vue";

let props = defineProps(["data", "bounds"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="badges_wrapper">

    <div class="poster_gradient"></div>

    <div class="badges_bar">

      <div class="rating_box">
        <h2 class="rating"> {{ data['user_rating'] }}</h2>
        <img :src="blue_star" alt="gold_star" class="gold_star">
      </div>

      <div class="rating_box" v-if="data['scaled_public_rating']>0">
        <h2 class="rating"> {{ Math.round(data['scaled_public_rating'] * 10) / 10 }}</h2>
        <img :src="gold_star" alt="gold_star" class="gold_star">
      </div>

      <rating-circle class="rating_circle" :text_size="(bounds[1]) * 0.005" v-if="data['scaled_public_rating']"
                     :score="(data['user_rating'] + data['scaled_public_rating'])/2"></rating-circle>

    </div>
  </div>
</template>

<style scoped>
.badges_wrapper {
  /*outline: 1px solid red;*/
  width: v-bind(bounds [0] + 'px');
  height: v-bind(bounds [1] + 'px');
  position: absolute;
  left: 0;
  top: 0;
  display: flex;

  /*font-family: monospace monospace;*/
}

.poster_gradient {
  content: "";
  position: absolute;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 90%, rgba(0, 0, 0, 0.5) 100%);
  left: 0;
  top: 0;
  height: 100%;
  width: 100%;
}

.rating_circle {
  height: calc(v-bind(bounds[1]) * 0.2px)
}

.badges_bar {
  /*outline: 1px solid red;*/
  position: absolute;
  display: flex;
  flex-flow: row nowrap;
  /*width: calc(v-bind(bounds[0]) * 1px);*/

  justify-content: flex-start;
  justify-items: center;
  align-content: center;
  align-items: center;

  padding: 5px;

  gap: 5px;
  bottom: 0;
  left: 0;

  transform: translate(0,50%);
}

.gold_star {
  width: calc(v-bind(bounds[1]) * 0.07px);;
  height: calc(v-bind(bounds[1]) * 0.07px);;
  /*height: 15px;*/
}

.rating_box {
  border-radius: 5px;

  box-shadow: 1px 1px 1px #000000;
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
  font-size: calc(v-bind(bounds[1]) * 0.005em);
  height: calc(v-bind(bounds[1]) * 0.0045em);
  font-weight: 500;
}

</style>