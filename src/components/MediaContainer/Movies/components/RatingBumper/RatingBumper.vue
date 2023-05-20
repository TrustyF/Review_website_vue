<script setup>
import {defineProps, defineEmits, watch, ref, onMounted} from 'vue'

import RatingTag from "@/components/MediaContainer/Movies/components/RatingBumper/RatingTag";

const props = defineProps(['data'])
const blue_star = './assets/ui/blue_star.png'
const gold_star = './assets/ui/gold_star.png'
const arrow_up_single = './assets/ui/arrow_up_single.png'
const arrow_up_double = './assets/ui/arrow_up_double.png'
const arrow_down_single = './assets/ui/arrow_down_single.png'
const arrow_down_double = './assets/ui/arrow_down_double.png'
const re_watch_down = './assets/ui/rewind_down.png'
const re_watch_up = './assets/ui/rewind_up.png'

function map_range(value, low1, high1, low2, high2) {
  return low2 + (high2 - low2) * (value - low1) / (high1 - low1);
}

const scaled_user_rating = ref(Math.round(map_range(props.data['vote_average'], 4.5, 9, 1, 10) * 10) / 10)
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

    <RatingTag :image="blue_star"
               :rating="data['my_rating']"
               name="My rating"
               :desc="`My rating is ${rating_diff} points higher than the scaled average rating`"
               :sub_desc="`The unscaled average rating is ${round_user_rating}`"
    ></RatingTag>

    <RatingTag :image="gold_star"
               :rating="scaled_user_rating"
               name="Average user rating"
               :desc="`My rating is ${rating_diff} points higher than the scaled average rating`"
               :sub_desc="`The unscaled average rating is ${round_user_rating}`"
    ></RatingTag>

    <RatingTag v-if="arrow_state===1"
               :image="arrow_up_single"
               name="Better than they say"
               :desc="`My rating is ${rating_diff} points higher than the scaled average imdb rating`"
               :sub_desc="`The unscaled imdb rating is ${round_user_rating}`"
    ></RatingTag>

    <RatingTag v-if="arrow_state===2"
               :image="arrow_up_double"
               name="Underrated"
               :desc="`My rating is ${rating_diff} points higher than the scaled average imdb rating`"
               :sub_desc="`The unscaled imdb rating is ${round_user_rating}`"
    ></RatingTag>

    <RatingTag v-if="arrow_state===3"
               :image="arrow_down_single"
               name="Underrated"
               :desc="`My rating is ${rating_diff} points lower than the scaled average imdb rating`"
               :sub_desc="`The unscaled imdb rating is ${round_user_rating}`"
    ></RatingTag>

    <RatingTag v-if="arrow_state===4"
               :image="arrow_down_double"
               name="Underrated"
               :desc="`My rating is ${rating_diff} points lower than the scaled average imdb rating`"
               :sub_desc="`The unscaled imdb rating is ${round_user_rating}`"
    ></RatingTag>

    <RatingTag v-if="data['re_watch']==='down'"
               :image="re_watch_down"
               name="Underrated"
               :desc="`My rating is ${rating_diff} points lower than the scaled average imdb rating`"
               :sub_desc="`The unscaled imdb rating is ${round_user_rating}`"
    ></RatingTag>

    <RatingTag v-if="data['re_watch']==='up'"
               :image="re_watch_up"
               name="Underrated"
               :desc="`My rating is ${rating_diff} points lower than the scaled average imdb rating`"
               :sub_desc="`The unscaled imdb rating is ${round_user_rating}`"
    ></RatingTag>


  </div>
</template>
<style scoped>
.bumper_wrapper {
  /*outline: red 1px solid;*/
  display: flex;
  flex-flow: row;
  gap: 3px;
  user-select: none;
}
</style>