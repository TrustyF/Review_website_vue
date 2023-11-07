<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import ExpandedFooterMobile from "@/components/MediaExpandedMobile/sub_components/ExpandedFooterMobile.vue";
import ExpandedHeaderMobile from "@/components/MediaExpandedMobile/sub_components/ExpandedHeaderMobile.vue";

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

const selected_media = inject("selected_media");


</script>

<template>
  <div class="media_expanded_wrapper">

    <div class="right">

      <img :src="data['poster_path']" class="poster" alt="poster" draggable="false">
      <expanded-header-mobile :data="data"></expanded-header-mobile>

    </div>

  </div>
</template>

<style scoped>
.media_expanded_wrapper {
  outline: 1px solid green;
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