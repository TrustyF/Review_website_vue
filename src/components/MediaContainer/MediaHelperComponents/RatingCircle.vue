<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["score", "old_score", "text_size"]);
const curr_api = inject("curr_api");

function get_rating_color(rating) {
  // if (rating >= 9){
  //   return '#00d0ff'
  // }
  if (rating >= 7) {
    return '#32cb1a'
  } else if (rating >= 5) {
    return '#e1c50f'
  } else if (rating >= 4) {
    return '#e17014'
  } else if (rating < 4) {
    return '#cb1a1a'
  }
}

</script>

<template>

  <div class="rating_circle_wrapper">

    <div class="progress-bar" :style="
    `background:
      radial-gradient(closest-side, #2b2a34 85%, transparent 90%),
      conic-gradient(${get_rating_color(score)} ${score * 10}%, ${'#595579'} 0);`
    ">


      <div class="text">
        <h1>{{ Math.round(score * 10) }}</h1>
        <h1 class="small_text">%</h1>
      </div>

    </div>

  </div>
</template>

<style scoped>

.rating_circle_wrapper {
}

.progress-bar {
  height: 100%;
  aspect-ratio: 1/1;
  border-radius: 50%;
  box-shadow: 1px 1px 2px black, 0 0 3px black;

  display: flex;
  justify-content: center;
  align-items: center;
}

.text {
  display: flex;
  justify-content: center;
  /*align-items: center;*/
}

h1 {
  color: white;
  font-weight: 500;
  font-size: calc(v-bind(text_size) * 0.0033em);
}

.small_text {
  font-size: calc(v-bind(text_size) * 0.002em);
  /*color: grey;*/
}
</style>