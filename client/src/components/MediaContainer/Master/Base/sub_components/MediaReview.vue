<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import RatingCircle from "@/components/MediaHelperComponents/RatingCircle.vue";
import TagBox from "@/components/MediaHelperComponents/TagBox.vue";

import gold_star from '@/assets/ui/gold_star.png'
import blue_star from '@/assets/ui/blue_star.png'

import arrow_down from '@/assets/ui/arrow_down_single.png'

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

</script>

<template>

  <div class="media_review_wrapper">

    <tag-box :score="data['user_rating']" :tag_img="blue_star"></tag-box>
    <tag-box :score="Math.round(data['scaled_public_rating'] * 10) / 10" :tag_img="gold_star"></tag-box>
<!--    <rating-circle :score="(data['user_rating'] + data['scaled_public_rating'])/2"></rating-circle>-->

  </div>

</template>

<style scoped>
.media_review_wrapper {
  /*outline: 1px solid cornflowerblue;*/
  width: 100%;
  height: 30px;
  display: flex;
  flex-flow: row wrap;
  align-items: center;
}
</style>