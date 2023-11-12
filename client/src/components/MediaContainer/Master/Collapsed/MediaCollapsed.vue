<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import CollapsedHeader from "./sub_components/CollapsedHeader.vue";
import RatingCircle from "@/components/MediaContainer/MediaHelperComponents/RatingCircle.vue";


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

<!--    <rating-circle class="rating_circle" :score="(data['user_rating'] + data['scaled_public_rating'])/2"></rating-circle>-->

    <div class="content">

      <div class="left_side">
        <img :src="data['poster_path']" class="poster" alt="poster" draggable="false">
      </div>

      <collapsed-header :data="data"></collapsed-header>

    </div>

  </div>
</template>

<style scoped>
.media_expanded_wrapper {
  /*outline: 1px solid green;*/
  /*height: 100%;*/
  /*height: 110px;*/
  position: relative;

  z-index: 2;

  padding: 7px;
  border-radius: 10px;
  background-color: #1c1b23;
}

.content {
  /*outline: 1px solid orange;*/

  /*width: 100%;*/
  height: 100%;
  /*min-width: 300px;*/
  display: flex;
  flex-flow: row nowrap;
  position: relative;
}
.left_side {
  position: relative;
  display: flex;
  flex-flow: column nowrap;
  align-items: center;
  gap: 5px;
}
.rating_circle {
  position: absolute;
  z-index: 25;
  left: 0;
  bottom: 0;
  height: 20px;
  width: 20px;
}

.poster {
  /*width: 50%;*/
  height: 100px;
  /*outline: 1px solid red;*/
  border-radius: 10px;
  object-fit: cover;
  box-shadow: 3px 3px 2px #131215;
}


</style>