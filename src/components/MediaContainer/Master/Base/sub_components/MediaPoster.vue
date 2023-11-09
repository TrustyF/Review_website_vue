<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaReview from "@/components/MediaContainer/Master/Base/sub_components/MediaReview.vue";

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

</script>

<template>

  <div class="media_poster_wrapper">
<!--    <img v-lazy="`https://image.tmdb.org/t/p/w500${data['poster_path']}`" class="poster" alt="poster" draggable="false">-->
    <img v-lazy="data['poster_path']" class="poster" alt="poster" draggable="false">
    <media-review class="review" :data="data"></media-review>
  </div>

</template>

<style scoped>
.media_poster_wrapper {
  /*outline: 1px solid red;*/
  position: relative;
  min-height: 225px;

}
.poster {
  height: 100%;
  width: 100%;
  object-fit: cover;
  border-radius: 8px 8px 0 0;
}

.review {
  position: absolute;
  /*right: 5px;*/
  bottom: -15px;
}
</style>