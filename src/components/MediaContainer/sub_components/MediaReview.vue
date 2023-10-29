<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import RatingCircle from "@/components/MediaHelperComponents/RatingCircle.vue";

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="media_review_wrapper">
    <rating-circle :score="data['user_rating']"></rating-circle>
    <rating-circle :score="data['public_rating']"></rating-circle>
  </div>
</template>

<style scoped>
.media_review_wrapper {
  /*outline: 1px solid yellow;*/
  display: flex;
  flex-flow: row nowrap;
  width: 40%;
  gap: 2px;
}
</style>