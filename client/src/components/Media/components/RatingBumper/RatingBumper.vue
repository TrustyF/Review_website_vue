<script setup>
import {defineProps, defineEmits, watch, ref, toRefs, onMounted, inject} from 'vue'

import RatingTag from "@/components/Media/components/RatingBumper/RatingTag";

const props = defineProps(['data', 'hover', 'mediaType'])
let hover = toRefs(props)['hover']
let mediaType = toRefs(props)['mediaType']
const forceVis = inject('forceVis')
const mediaRanges = inject('mediaRanges')

const blue_star = './assets/ui/blue_star.png'
const gold_star = './assets/ui/gold_star.png'
const arrow_up_single = './assets/ui/arrow_up_single.png'
const arrow_up_double = './assets/ui/arrow_up_double.png'
const arrow_down_single = './assets/ui/arrow_down_single.png'
const arrow_down_double = './assets/ui/arrow_down_double.png'
const re_watch_down = './assets/ui/rewind_down.png'
const re_watch_up = './assets/ui/rewind_up.png'
const re_read = './assets/ui/reading.png'
const stop = './assets/ui/stop.png'

let ratingDesc = {
  9: 'Near perfect masterpiece',
  8: 'Extremely good',
  7: 'Quite good',
  6: 'Good with flaws',
  5: "Meh",
  4: 'Bad',
  3: 'Fucking bad',
  2: 'Holy shit bad',
  1: 'Affront to god',
}
let avg_range = [1, 10]
let my_range = [1, 10]

function map_range(value, low1, high1, low2, high2) {
  return low2 + (high2 - low2) * (value - low1) / (high1 - low1);
}

const scaled_user_rating = ref(0)
const round_user_rating = ref(0)

let rating_diff = 0

const arrow_state = ref(0)


function calc() {

  if (props.data['dropped'] === 'on') return

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

onMounted(() => {
  if (mediaRanges.value[mediaType.value]['avg_range'] !== undefined) {
    avg_range = mediaRanges.value[mediaType.value]['avg_range']
    my_range = mediaRanges.value[mediaType.value]['my_range']
  }

  scaled_user_rating.value = (Math.round(map_range(props.data['vote_average'], avg_range[0], avg_range[1], Number(my_range[0]), 10) * 10) / 10)
  round_user_rating.value = (Math.round(props.data['vote_average'] * 10) / 10)

  rating_diff = Math.abs(props.data['my_rating'] - scaled_user_rating.value).toFixed(0)

  calc()
  if (forceVis.value) {
    // console.log('bumper', forceVis.value)
    hover = forceVis.value
  }
})

</script>


<template>
  <div class="bumper_wrapper">

    <RatingTag :image="blue_star"
               :rating="data['my_rating']"
               :desc="data['my_rating'] + ': ' + ratingDesc[data['my_rating']]"
               sub_desc="The most important metric"
               name="My personal rating"
               style="visibility: visible;opacity: 100%"
    ></RatingTag>

    <RatingTag :image="gold_star"
               :class="hover ? 'extras hover' : 'extras'"
               :rating="scaled_user_rating"
               name="Average user rating"
               :desc="`The unscaled average rating is ${round_user_rating}`"
               :sub_desc="`The average rating is mapped from between ${avg_range[0]} and ${avg_range[1]}, to ${my_range[0]} and 10`"
    ></RatingTag>

    <RatingTag v-if="arrow_state===1"
               :class="hover ? 'extras hover' : 'extras'"
               :image="arrow_up_single"
               name="Better than they say"
               :desc="`My rating is ${rating_diff} points higher than the scaled average rating`"
               :sub_desc="`The unscaled average rating is ${round_user_rating}`"
    ></RatingTag>

    <RatingTag v-if="arrow_state===2"
               :class="hover ? 'extras hover' : 'extras'"
               :image="arrow_up_double"
               name="Underrated"
               :desc="`My rating is ${rating_diff} points higher than the scaled average rating`"
               :sub_desc="`The unscaled average rating is ${round_user_rating}`"
    ></RatingTag>

    <RatingTag v-if="arrow_state===3"
               :class="hover ? 'extras hover' : 'extras'"
               :image="arrow_down_single"
               name="Not that good"
               :desc="`My rating is ${rating_diff} points lower than the scaled average rating`"
               :sub_desc="`The unscaled average rating is ${round_user_rating}`"
    ></RatingTag>

    <RatingTag v-if="arrow_state===4"
               :class="hover ? 'extras hover' : 'extras'"
               :image="arrow_down_double"
               name="Overrated"
               :desc="`My rating is ${rating_diff} points lower than the scaled average rating`"
               :sub_desc="`The unscaled average rating is ${round_user_rating}`"
    ></RatingTag>

    <RatingTag v-if="data['dropped']==='on'"
               :class="hover ? 'extras hover' : 'extras'"
               :image="stop"
               name="Unfinished"
               desc="Did not get around to finishing it or outright dropped it"
    ></RatingTag>

    <RatingTag v-if="data['re_watch']==='down'"
               :class="hover ? 'extras hover' : 'extras'"
               :image="re_watch_down"
               name="Watch-listed"
               desc="Unsure about this rating, will probably be adjusted down after a re-watch."
    ></RatingTag>

    <RatingTag v-if="data['re_watch']==='up'"
               :class="hover ? 'extras hover' : 'extras'"
               :image="re_watch_up"
               name="Watch-listed"
               desc="Unsure about this rating, will probably be adjusted down after a re-watch."
    ></RatingTag>

    <RatingTag v-if="data['re_read']"
               :class="hover ? 'extras hover' : 'extras'"
               :image="re_read"
               name="Inexhaustible entertainment"
               :desc="`I re-read this one ${data['re_read']} times because of how good it was`"
               :number="data['re_read']"
    ></RatingTag>

    <RatingTag v-if="data['contentRating']==='suggestive'"
               :class="hover ? 'extras hover' : 'extras'"
               rating="+13"
               name="Suggestive"
               desc="Sexual themes are present in this story"
    ></RatingTag>

    <RatingTag v-if="data['contentRating']==='erotica'"
               :class="hover ? 'extras hover' : 'extras'"
               rating="+18"
               name="Erotic"
               desc="Sex plays a major part in the story, and shows up frequently"
    ></RatingTag>

    <RatingTag v-if="data['contentRating']==='pornographic'"
               :class="hover ? 'extras hover' : 'extras'"
               rating="+18"
               name="Pornographic"
               desc="Porn, its porn..."
    ></RatingTag>

    <RatingTag v-if="data['hours_played']!==undefined"
               :class="hover ? 'extras hover' : 'extras'"
               :rating="`${data['hours_played']=== 999 ?  '10 years' : data['hours_played'] + ' hours'}`"
               name="Playtime"
               desc="How much of my life I lost to this"
    ></RatingTag>

  </div>
</template>
<style scoped>
.bumper_wrapper {
  display: flex;
  flex-flow: row;
  align-items: center;
  user-select: none;
  gap: 3px;
  /*outline: blue 1px solid;*/
}

.extras {
  /*outline: 1px solid yellow;*/
  transform: translate(0px, 20px);
  transition: 50ms ease-in-out;
  transition-delay: 50ms;

  visibility: hidden;
  opacity: 0;
}

.hover {
  transform: translate(0px, 0px);
  transition-delay: 0ms;

  visibility: visible;
  opacity: 100%;
}
</style>