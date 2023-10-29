<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["score", "tag_img"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="tag_box_wrapper">
    <h1>{{ score }}</h1>
    <img :src="tag_img" alt="tag_image" class="tag_image">
  </div>
</template>

<style scoped>
.tag_box_wrapper {
  /*outline: 1px solid yellow;*/
  padding: 0 5px 0 5px;
  display: flex;
  justify-items: center;
  align-items: center;
  background-color: #41404d;
  border-radius: 5px;
  height: 70%;
  font-size: 0.8em;
  box-shadow: 1px 2px 0 #1c1b23;
  margin: 3px;
}
.tag_image {
  height: 70%;
}
</style>