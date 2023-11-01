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

    <div class="right">

      <img :src="`https://image.tmdb.org/t/p/w500${selected_media['poster_path']}`" class="poster" alt="poster"
           draggable="false">
      <expanded-header :data="selected_media"></expanded-header>

    </div>
<!--    <expanded-footer :data="selected_media"></expanded-footer>-->

  </div>
</template>

<style scoped>
.media_expanded_wrapper {
  /*outline: 3px solid green;*/
  height: 100%;
  width: 100%;

  z-index: 2;
  /*display: flex;*/
  /*flex-flow: column wrap;*/
}

.right {
  height: 100%;
  /*width: 100%;*/
  display: flex;
  flex-flow: row nowrap;
}

.poster {
  height: 100%;
  /*outline: 1px solid red;*/
  border-radius: 10px;
  object-fit: contain;
  box-shadow: 3px 3px 2px #131215;
}
</style>