<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["score"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="rating_circle_wrapper">

    <div class="progress-bar" :style="
    `background:
      radial-gradient(closest-side, #2b2a34 80%, transparent 81%),
      conic-gradient(${score > 5 ? score > 7.5 ? '#27ae60' : '#f1c40f' : '#e74c3c'} ${score * 10}%, #2b2a34 0);`
    ">
      <h1>{{ Math.round(score * 10) }}</h1>
      <h1 class="small_text">%</h1>
    </div>

  </div>
</template>

<style scoped>

.rating_circle_wrapper{
  /*outline: 1px solid red;*/
  display: flex;
  width: 100%;
  aspect-ratio: 1/1;
}
.progress-bar {
  aspect-ratio: 1/1;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}
h1 {
  /*position: absolute;*/
  color: white;
  font-weight: bold;
  font-size: 1.8vw;
  text-align: center;
  transform: translate(0,0.5px);
}
.small_text {
  font-size: 1vw;
  /*color: grey;*/
}
</style>