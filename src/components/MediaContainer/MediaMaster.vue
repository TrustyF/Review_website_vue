<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaPoster from "@/components/MediaContainer/sub_components/MediaPoster.vue";

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

</script>

<template>

  <div class="wrapper">{{data}}
<!--    <media-poster :data="data"></media-poster>-->

  </div>

</template>

<style scoped>
.wrapper {
  outline: 1px solid green;

  width: 200px;
  height: 350px;
  /*height: fit-content;*/
  position: relative;
  color: white;

  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);

  background-color: #2b2a34;

  /*overflow: hidden;*/
  transition: 0.2s ease;

  display: flex;
}
</style>