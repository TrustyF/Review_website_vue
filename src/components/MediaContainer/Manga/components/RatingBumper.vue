<script setup>
import {defineProps, defineEmits, watch, ref, onMounted} from 'vue'

const props = defineProps(['data'])
const arrow_up_single = './assets/ui/arrow_up_single.png'
const arrow_up_double = './assets/ui/arrow_up_double.png'
const arrow_down_single = './assets/ui/arrow_down_single.png'
const arrow_down_double = './assets/ui/arrow_down_double.png'
const re_watch_down = './assets/ui/rewind_down.png'
const re_watch_up = './assets/ui/rewind_up.png'

function map_range(value, low1, high1, low2, high2) {
  return low2 + (high2 - low2) * (value - low1) / (high1 - low1);
}

const scaled_user_rating = ref(Math.round(map_range(props.data['vote_average'], 4, 9.5, 0, 5) * 10) / 10)
const round_user_rating = ref(Math.round(props.data['vote_average'] * 10) / 10)

const rating_diff = Math.abs(props.data['my_rating'] - scaled_user_rating.value).toFixed(0)

const arrow_state = ref(0)

calc()

function calc() {
  if (props.data['my_rating'] > scaled_user_rating.value + 1.5) {
    arrow_state.value = 1
    if (props.data['my_rating'] > scaled_user_rating.value + 2.5) {
      arrow_state.value = 2
    }
    return
  }
  if (props.data['my_rating'] < scaled_user_rating.value - 1.5) {
    arrow_state.value = 3
    if (props.data['my_rating'] < scaled_user_rating.value - 2.5) {
      arrow_state.value = 4
    }
    return
  }
  arrow_state.value = 0
}


</script>

<template>
  <div class="bumper_wrapper">
    <p class="rating star_blue">{{ data['my_rating'] }} </p>
    <p class="rating star_gold">{{ scaled_user_rating }} </p>
    <!--    <p class="rating star_gold">{{ round_user_rating }} </p>-->
    <!--    <p class="rating ">{{ props['rating'] }} </p>-->
    <!--    <p class="rating ">{{ props['user_rating'] }} </p>-->


    <div v-if="arrow_state===1" class="tooltip">
      <img class="rating arrow" v-lazy="arrow_up_single">
      <div class="hover_box">
        <div class="description">
          <h1 class="tag_name">Better than they say</h1>
          <h1 class="tag_description">My rating is {{ rating_diff }} points higher than the scaled average rating</h1>
          <h1 class="tag_description" style="font-size: 0.6em;margin-top: 5px;  color: rgba(0, 0, 0, 0.4);">
            {{ "The unscaled average rating is: " + round_user_rating }}</h1>
        </div>
      </div>
    </div>

    <div v-if="arrow_state===2" class="tooltip">
      <img class="rating arrow" v-lazy="arrow_up_double">
      <div class="hover_box">
        <div class="description">
          <h1 class="tag_name">Underrated</h1>
          <h1 class="tag_description">My rating is {{ rating_diff }} points higher than the scaled average rating</h1>
          <h1 class="tag_description" style="font-size: 0.6em;margin-top: 5px;  color: rgba(0, 0, 0, 0.4);">
            {{ "The unscaled average rating is: " + round_user_rating }}</h1>
        </div>
      </div>
    </div>

    <div v-if="arrow_state===3" class="tooltip">
      <img class="rating arrow" v-lazy="arrow_down_single" style="transform: rotate(180deg)">
      <div class="hover_box">
        <div class="description">
          <h1 class="tag_name">Not that good</h1>
          <h1 class="tag_description">My rating is {{ rating_diff }} points lower than the scaled average rating</h1>
          <h1 class="tag_description" style="font-size: 0.6em;margin-top: 5px;  color: rgba(0, 0, 0, 0.4);">
            {{ "The unscaled average rating is: " + round_user_rating }}</h1>
        </div>
      </div>
    </div>

    <div v-if="arrow_state===4" class="tooltip">
      <img class="rating arrow" v-lazy="arrow_down_double" style="transform: rotate(180deg)">
      <div class="hover_box">
        <div class="description">
          <h1 class="tag_name">Overrated</h1>
          <h1 class="tag_description">My rating is {{ rating_diff }} points lower than the scaled average rating</h1>
          <h1 class="tag_description" style="font-size: 0.6em;margin-top: 5px;  color: rgba(0, 0, 0, 0.4);">
            {{ "The unscaled average rating is: " + round_user_rating }}</h1>
        </div>
      </div>
    </div>

    <div v-if="data['re_watch']==='down'" class="tooltip">
      <img class="rating arrow" v-lazy="re_watch_down">
      <div class="hover_box">
        <div class="description">
          <h1 class="tag_name">Watch listed</h1>
          <h1 class="tag_description">I'm not too sure about the current rating, will probably be adjusted <strong> down </strong> after
            re-reading</h1>
        </div>
      </div>
    </div>

    <div v-if="data['re_watch']==='up'" class="tooltip">
      <img class="rating arrow" v-lazy="re_watch_up" style="transform: rotate(180deg)">
      <div class="hover_box">
        <div class="description">
          <h1 class="tag_name">Watch listed</h1>
          <h1 class="tag_description">I'm not too sure about the current rating, will probably be adjusted <strong> up</strong> after
            re-reading</h1>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "RatingBumperManga"
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
  background-color: rgba(255, 255, 255, 1);
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.5);

  /*color: white;*/
  font-size: 0.8em;
  padding: 3px;
  border-radius: 5px;
}

.arrow {
  height: 100%;
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
}

.hover_box {
  position: absolute;
  left: 0;
  top: 0;
  transform: translate(-101px, -90px);
  background-color: white;
  padding: 10px;
  border-radius: 5px;
  filter: drop-shadow(0px 0 2px rgba(0, 0, 0, 0.5));

  /*outline: 2px red solid;*/
  visibility: hidden;
  opacity: 0;
  transition: 0.1s ease-in-out;
}

.hover_box:after {
  content: '';
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
  /*outline: 1px solid blue;*/
  height: 0.8em;
}

.tag_name {
  font-size: 0.9em;
  margin-bottom: 5px;
  /*text-decoration: underline;*/
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