<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaPoster from "@/components/MediaContainer/Master/Base/sub_components/MediaPoster.vue";
import MediaFooter from "@/components/MediaContainer/Master/Base/sub_components/MediaFooter.vue";

let props = defineProps(["data"]);

const curr_api = inject("curr_api");
const selected_media = inject("selected_media");

function emit_selected_media(media) {
  console.log('selecting media ' + media['name'])
  selected_media.value = media
}
</script>

<template>

  <div class="media_master_wrapper" @click="emit_selected_media(data)">
    <media-poster :data="data"></media-poster>
    <media-footer :data="data"></media-footer>
  </div>

</template>

<style scoped>
.media_master_wrapper {
  /*outline: 1px solid green;*/
  max-width: 150px;

  position: relative;
  color: white;

  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);

  background-color: #2b2a34;

  /*overflow: hidden;*/
  transition: 0.2s ease;

  display: flex;
  flex-flow: column nowrap;
  /*outline: 0.1em #5b5b5b solid;*/
}
</style>