<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import gold_star from '@/assets/ui/gold_star.png'
import blue_star from '@/assets/ui/blue_star.png'
import RatingCircle from "@/components/MediaHelperComponents/RatingCircle.vue";

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

</script>

<template>
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


    <rating-circle class="rating_circle" :score="(data['user_rating'] + data['scaled_public_rating'])/2"></rating-circle>

  </div>
</template>

<style scoped>

.rating_circle {
  /*position: absolute;*/
  /*z-index: 25;*/
  /*left: 0;*/
  /*bottom: 0;*/
  height: 20px;
  width: 20px;
}
.ratings_wrapper {
  /*width: 100%;*/
  /*height: 20px;*/
  /*outline: 1px solid red;*/
  display: flex;
  flex-flow: row nowrap;
  /*justify-content: space-between;*/
  gap: 5px;
}
.gold_star {
  width: 10px;
  height: 10px;
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
  background-color: #2d2d41;

  padding: 3px 5px 3px 5px;

  display: flex;
  flex-flow: row nowrap;
  text-align: center;

  align-items: center;

  gap: 2px;
}

.rating {
  font-size: 0.6em;
  height: 0.8em;
  font-weight: 500;
}
</style>