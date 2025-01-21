<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["color"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

</script>

<template>
    <div v-if="color==='red'" style="background-color: rgb(204,52,41)" class="tag_box"/>
    <div v-if="color==='green'" style="background-color: rgb(36,179,93)" class="tag_box"/>
    <div v-if="color==='purple'" style="background-color: rgb(179,36,177)" class="tag_box"/>
    <div v-if="color==='gold'" style="background-color: rgb(217,194,43)" class="tag_box"/>
    <div v-if="color==='grey'" style="background-color: rgb(179,179,179)" class="tag_box"/>
</template>

<style scoped>
.tag_box {
  width:5px;
  aspect-ratio: 1;
  border-radius: 50%;

  display: flex;
  align-items: center;

  /*border: 1px solid rgba(0, 0, 0, 0.7);*/
  /*box-shadow: 0 0 1px #1c1b23;*/
  /*opacity: 0.7;*/
}
</style>