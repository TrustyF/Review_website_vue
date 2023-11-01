<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaExpanded from "@/components/MediaExpanded/MediaExpanded.vue";

let props = defineProps(["test"]);
const curr_api = inject("curr_api");
const selected_media = ref(undefined)

</script>

<template>

  <div class="media_pane_wrapper">
    <div class="feed">
      <media-expanded :data="selected_media"></media-expanded>
    </div>
  </div>

</template>

<style scoped>
.media_pane_wrapper {
  position: fixed;
  bottom: 50px;
  left: 50px;
  width: 70%;
  height: 30%;
  outline: 3px deeppink solid;
  z-index: 2;
  background-color: black;
  /*display: flex;*/
}
.feed {
  /*width: 100%;*/
  /*height: 100%;*/
  margin: 50px;
  outline: 5px greenyellow solid;
}
</style>