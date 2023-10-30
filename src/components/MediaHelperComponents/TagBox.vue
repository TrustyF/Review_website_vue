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
  /*background-color: #41404d;*/
  background-color: #2b2a34;
  border-radius: 5px;
  height: 70%;
  font-size: 0.8em;
  box-shadow: 1px 1px 2px black,0 0 3px black;
  margin: 3px;
}
.tag_image {
  height: 70%;
}
h1 {
  color: white;
  /*font-weight: bold;*/
  font-size: 1em;
}
</style>