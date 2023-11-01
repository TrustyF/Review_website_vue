<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import gold_star from '@/assets/ui/gold_star.png'

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="ratings_wrapper">
    <div class="my_rating">
      <h1> My rating:</h1>
      <div class="rating_box">
        <h2 class="rating"> {{ data['user_rating'] }}</h2>
        <img :src="gold_star" alt="gold_star" class="gold_star">
      </div>
    </div>

    <div class="my_rating">
      <h1> Public rating:</h1>
      <div class="rating_box">
        <h2 class="rating"> {{ Math.round(data['scaled_public_rating'] * 10) / 10 }}</h2>
        <img :src="gold_star" alt="gold_star" class="gold_star">
      </div>
    </div>
  </div>
</template>

<style scoped>
.ratings_wrapper {
  /*width: 100%;*/
  height: 20px;
  /*outline: 1px solid red;*/
  display: flex;
  flex-flow: row nowrap;
  gap: 10px;
}

h1 {
  font-size: 0.8em;
  /*color: grey;*/
}

.gold_star {
  width: 15px;
  height: 15px;
}

.my_rating {
  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  gap: 10px;
}

.rating_box {
  outline: 1.5px solid grey;
  border-radius: 7px;
  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  padding: 4px 6px 4px 6px;
  box-shadow: 2px 2px 5px #000000;
}

.rating {
  font-size: 0.8em;
  /*font-weight: bold;*/
  transform: translate(0, 0.5px);
}
</style>