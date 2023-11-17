<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import gold_star from '@/assets/ui/gold_star.png'
import blue_star from '@/assets/ui/blue_star.png'
import RatingCircle from "@/components/MediaContainer/MediaHelperComponents/RatingCircle.vue";

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

</script>

<template>

  <div class="media_poster_wrapper">

    <img v-lazy="data['poster_path']" class="poster" alt="poster" draggable="false">

    <div class="poster_gradient"></div>

    <div class="ratings_wrapper">
      <div class="my_rating">
        <!--      <h1> My rating:</h1>-->
        <div class="rating_box">
          <h2 class="rating"> {{ data['user_rating'] }}</h2>
          <img :src="blue_star" alt="gold_star" class="gold_star">
        </div>
      </div>

      <div class="my_rating">
        <!--      <h1> Public rating:</h1>-->
        <div class="rating_box">
          <h2 class="rating"> {{ Math.round(data['scaled_public_rating'] * 10) / 10 }}</h2>
          <img :src="gold_star" alt="gold_star" class="gold_star">
        </div>
      </div>

      <rating-circle class="rating_circle" :text_size="1.5"
                     :score="(data['user_rating'] + data['scaled_public_rating'])/2"></rating-circle>

    </div>

  </div>

</template>

<style scoped>
.media_poster_wrapper {
  outline: 1px solid red;
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
}

.poster {
  width: 100%;
  object-fit: cover;
  border-radius: 8px 8px 0 0;
}

.poster_gradient {
  content: "";
  /*outline: 1px solid red;*/
  position: absolute;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 90%, rgba(0, 0, 0, 0.5) 100%);
  left: 0;
  top: 0;
  height: 100%;
  width: 100%;
}

.rating_circle {
  height: 30px;
  /*width: 20px;*/
}

.ratings_wrapper {
  position: absolute;
  display: flex;
  flex-flow: row nowrap;
  gap: 5px;
  bottom: -15px;
  left: 5px;
}

.gold_star {
  width: 12px;
  height: 12px;
}

.my_rating {
  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  gap: 5px;
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
  font-size: 0.8em;
  height: 0.8em;
  font-weight: 500;
}

</style>