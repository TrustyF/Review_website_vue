<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import ExpandedHeader from "@/components/MediaExpanded/sub_components/ExpandedHeader.vue";
import ExpandedFooter from "@/components/MediaExpanded/sub_components/ExpandedFooter.vue";

let props = defineProps(["test"]);
const curr_api = inject("curr_api");

const selected_media = inject("selected_media");


</script>

<template>
  <div class="media_expanded_wrapper" v-if="selected_media!==undefined">


    <img :src="`https://image.tmdb.org/t/p/w500${selected_media['poster_path']}`" class="poster" alt="poster"
         draggable="false">


<!--    <div class="right">-->
<!--      <expanded-header :data="selected_media"></expanded-header>-->
<!--      <expanded-footer :data="selected_media"></expanded-footer>-->
<!--    </div>-->

  </div>
</template>

<style scoped>
.media_expanded_wrapper {
  outline: 3px solid green;
  height: 100%;
  width: 100%;
  /*bottom: 0;*/
  background: rgba(0, 0, 0, 1);
  z-index: 2;
  /*display: flex;*/
}
.right {
  height: 100%;
  width: 100%;
  display: flex;
  flex-flow: column nowrap;
}
.poster {
  height: 100%;
  outline: 1px solid red;
  object-fit: contain;
}
</style>