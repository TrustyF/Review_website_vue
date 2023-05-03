<script setup>
import {defineProps, defineEmits, ref, watch, onMounted} from 'vue'

const props = defineProps(['rating', 'user_rating'])

const scaled_user_rating = Math.round(map_range(props['user_rating'], 4.5, 9, 1, 10) * 10) / 10
const round_user_rating = Math.round(props['user_rating'] * 10) / 10

const arrow_state = ref(0)

function map_range(value, low1, high1, low2, high2) {
  return low2 + (high2 - low2) * (value - low1) / (high1 - low1);
}

onMounted(() => {
  if (props['rating'] > scaled_user_rating + 1.5) {
    arrow_state.value = 1
  } else if (props['rating'] < scaled_user_rating - 3) {
    arrow_state.value = 2
  }
})
</script>

<template>
  <div class="bumper_wrapper">
    <p class="rating star_blue">{{ rating }} </p>
    <p class="rating star_gold">{{ scaled_user_rating }} </p>

    <div v-if="arrow_state===1" class="tooltip">
    <p class="rating green">🡅</p>
    <div class="hover_box">
      <div class="description">
        <h1 class="tag_description">My rating is 1.5 points higher than the scaled average imdb rating</h1>
        <h1 class="tag_description" style="font-size: 0.6em;margin-top: 5px;  color: rgba(0, 0, 0, 0.4);">{{ "The unscaled imdb rating is: " + round_user_rating }}</h1>
      </div>
    </div>
    </div>

    <div v-if="arrow_state===2" class="tooltip">
      <p class="rating red">🡅</p>
      <div class="hover_box">
        <div class="description">
          <h1 class="tag_description">My rating is 3 points lower than the scaled average imdb rating</h1>
          <h1 class="tag_description" style="font-size: 0.6em;margin-top: 5px;  color: rgba(0, 0, 0, 0.4);">{{ "The unscaled imdb rating is: " + round_user_rating }}</h1>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RatingBumperV2"
}
</script>
<style scoped>
.bumper_wrapper {
  /*outline: red 1px solid;*/
  display: flex;
  flex-flow: row;
  gap: 3px;
  user-select: none;
}

.rating {
  width: min-content;
  /*background-color: rgba(1,1,1,0.8);*/
  background-color: rgba(255, 255, 255, 1);
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.5);

  /*color: white;*/
  font-size: 0.7em;
  padding: 3px;
  border-radius: 5px;
}

.star_blue::after {
  content: "★";
  color: dodgerblue;
}

.star_gold::after {
  content: "★";
  color: #ffc900;
}

.green {
  color: #00c000;
}

.red {
  color: #ff3f27;
  transform: rotate(180deg);
}
.hover_box {
  position: absolute;
  left: 0;
  top: 0;
  transform: translate(-102px,-70px);
  background-color: white;
  padding: 10px;
  border-radius: 5px;
  filter: drop-shadow(0px 0 2px rgba(0, 0, 0, 0.5));

  visibility: hidden;
  opacity: 0;
  transition: 0.1s ease-in-out;
}
.hover_box:after {
  content:'';
  position: absolute;
  left: 0;
  right: 0;
  margin: 10px auto;
  width: 0;
  height: 0;
  border-top: 5px solid white;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
}

.tooltip:hover .hover_box {
  visibility: visible;
  opacity: 100%;
}
.tooltip {
  display: inline-block;
  position: relative;
  text-align: left;
}
.tag_description {
  /*outline: 1px solid red;*/
  font-size: 0.7em;
  text-align: left;
  margin: 0;
  width: 200px;
  color: rgba(0, 0, 0, 0.6);
  overflow-wrap: break-word;
}
</style>