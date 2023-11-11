<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import CollapsedHeader from "./sub_components/CollapsedHeader.vue";
import CollapsedHeaderRating
  from "@/components/MediaContainer/Master/Collapsed/sub_components/CollapsedHeaderRating.vue";


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

    <div class="content">

      <img :src="data['poster_path']" class="poster" alt="poster" draggable="false">
      <collapsed-header :data="data"></collapsed-header>

      <div class="collapsed_rating_wrapper">
        <collapsed-header-rating :data="data"></collapsed-header-rating>
      </div>


    </div>

  </div>
</template>

<style scoped>
.media_expanded_wrapper {
  /*outline: 1px solid green;*/
  height: 100%;

  z-index: 2;

  padding: 7px;
  border-radius: 5px;
  background-color: #1c1b23;
}

.content {
  /*outline: 1px solid orange;*/

  max-height: 150px;
  /*width: 100%;*/
  min-width: 300px;
  display: flex;
  flex-flow: row nowrap;
  position: relative;
}

.poster {
  max-height: 150px;
  /*outline: 1px solid red;*/
  border-radius: 10px;
  object-fit: contain;
  box-shadow: 3px 3px 2px #131215;
}

.collapsed_rating_wrapper {
  position: absolute;
  left: 2px;
  bottom: 4px;
  /*outline: 1px solid red;*/
  margin-top: auto;
}
</style>