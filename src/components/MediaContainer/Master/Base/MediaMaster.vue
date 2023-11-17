<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaPoster from "@/components/MediaContainer/Master/Base/sub_components/MediaPoster.vue";
import MediaFooter from "@/components/MediaContainer/Master/Base/sub_components/MediaFooter.vue";

let props = defineProps(["data"]);

const curr_api = inject("curr_api");
const selected_media = inject("selected_media");
let container_width = ref('150px')

function fit_container_to_media(){
  if (props['data']['media_type'] === 'short'){
    container_width.value = "320px"
  }
}

function emit_selected_media(media) {
  console.log('selecting media ' + media['name'])
  selected_media.value = media
}

onMounted(()=>{
  fit_container_to_media()
})
</script>

<template>

  <div class="media_master_wrapper" id="media_container" @click="emit_selected_media(data)">
    <media-poster :data="data"></media-poster>
    <media-footer :data="data"></media-footer>
  </div>

</template>

<style scoped>
.media_master_wrapper {
  /*outline: 1px solid red;*/

  position: relative;
  color: white;

  width: v-bind(container_width);

  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);

  background-color: #2b2a34;

  display: flex;
  flex-flow: column nowrap;
}
</style>