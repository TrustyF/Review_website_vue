<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaPoster from "@/components/MediaContainer/Master/Base/sub_components/MediaPoster.vue";
import MediaFooter from "@/components/MediaContainer/Master/Base/sub_components/MediaFooter.vue";

let props = defineProps(["data"]);

const curr_api = inject("curr_api");
const selected_media = inject("selected_media");
const edit_media = inject("edit_media");
const edit_mode = inject("edit_mode");

let container_width = ref('150px')
let container_height = ref('225px')

function fit_container_to_media() {
  if (props['data']['media_type'] === 'short') {
    container_width.value = "320px"
    container_height.value = "165px"
  }
  if (props['data']['media_type'] === 'game') {
    container_width.value = "150px"
    container_height.value = "200px"
  }
  if (props['data']['media_type'] === 'manga') {
    container_width.value = "150px"
    container_height.value = "215px"
  }
}

function emit_selected_media(media) {
  console.log('selecting media ' + media['name'])
  selected_media.value = media
}

function emit_edit_media(media) {
  console.log('edit media ' + media['name'])
  edit_media.value = media
}

onMounted(() => {
  fit_container_to_media()
})
</script>

<template>

  <div class="media_master_wrapper" id="media_container" @click.stop="emit_selected_media(data)">

    <button v-if="edit_mode" class="edit_button" @click.stop="emit_edit_media(data)">edit</button>

    <img v-lazy="`${curr_api}/media/get_image?id=${data['id']}`" class="poster" alt="poster" draggable="false">

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
.edit_button {
  position: absolute;
}
.poster {
  height: v-bind(container_height);

  object-fit: cover;
  border-radius: 8px 8px 0 0;
}
</style>