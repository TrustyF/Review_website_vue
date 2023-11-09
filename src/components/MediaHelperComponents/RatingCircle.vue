<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["score", "old_score"]);
const curr_api = inject("curr_api");

function get_rating_color(rating){

  if (rating >= 7){
    return '#32cb1a'
  }
  else if (rating >= 5){
    return '#e1c50f'
  }
  else if (rating >= 4){
    return '#e17014'
  }
  else if (rating < 4){
    return '#cb1a1a'
  }
}

</script>

<template>

    <div class="rating_circle_wrapper">

      <div class="progress-bar" :style="
    `background:
      radial-gradient(closest-side, #2b2a34 80%, transparent 85%),
      conic-gradient(${get_rating_color(score)} ${score * 10}%, ${'#595579'} 0);`
    ">

        <h1>{{ Math.round(score * 10) }}</h1>
        <h1 class="small_text">%</h1>
      </div>

    </div>
</template>

<style scoped>

.rating_circle_wrapper {
  /*outline: 1px solid red;*/
  display: flex;
  height: 100%;
  aspect-ratio: 1/1;
  margin: 3px;

}

.progress-bar {
  height: 100%;
  aspect-ratio: 1/1;
  border-radius: 50%;
  box-shadow: 1px 1px 2px black,0 0 3px black;

  display: flex;
  justify-content: center;
  align-items: center;
}

h1 {
  /*position: absolute;*/
  color: white;
  font-weight: bold;
  font-size: 0.8em;
  text-align: center;
  transform: translate(0.5px, 1px);
}

.small_text {
  font-size: 0.5em;
  /*color: grey;*/
}
</style>