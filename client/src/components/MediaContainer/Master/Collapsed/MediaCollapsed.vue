<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import CollapsedHeader from "./sub_components/CollapsedHeader.vue";

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

const selected_media = inject("selected_media");

function emit_selected_media(media) {
  console.log('selecting media ' + media['name'])
  selected_media.value = media
}

</script>

<template>
  <div class="media_expanded_wrapper" @click="emit_selected_media(data)">

    <div class="right">

      <img :src="data['poster_path']" class="poster" alt="poster" draggable="false">
      <collapsed-header :data="data"></collapsed-header>

    </div>

  </div>
</template>

<style scoped>
.media_expanded_wrapper {
  /*outline: 1px solid green;*/
  height: 100%;
  width: 100%;

  z-index: 2;
  /*display: flex;*/
  /*flex-flow: column wrap;*/
}

.right {
  /*outline: 1px solid green;*/

  height: 100%;
  /*width: 100%;*/
  min-width: 300px;
  display: flex;
  flex-flow: row nowrap;
}

.poster {
  max-height: 150px;
  /*outline: 1px solid red;*/
  border-radius: 10px;
  object-fit: contain;
  box-shadow: 3px 3px 2px #131215;
}
</style>