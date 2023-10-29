<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaPoster from "@/components/MediaContainer/sub_components/MediaPoster.vue";
import MediaFooter from "@/components/MediaContainer/sub_components/MediaFooter.vue";
import MediaReview from "@/components/MediaContainer/sub_components/MediaReview.vue";

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

</script>

<template>

  <div class="wrapper">
    <media-poster :data="data"></media-poster>
    <media-footer :data="data"></media-footer>
  </div>

</template>

<style scoped>
.wrapper {
  /*outline: 1px solid green;*/

  width: 150px;

  position: relative;
  color: white;

  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);

  background-color: #2b2a34;

  /*overflow: hidden;*/
  transition: 0.2s ease;

  display: flex;
  flex-flow: column nowrap;
}
</style>