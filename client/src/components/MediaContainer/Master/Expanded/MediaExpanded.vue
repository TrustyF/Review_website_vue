<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import ExpandedHeader from "@/components/MediaContainer/Master/Expanded/sub_components/ExpandedHeader.vue";
import ExpandedFooter from "@/components/MediaContainer/Master/Expanded/sub_components/ExpandedFooter.vue";

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

const selected_media = inject("selected_media");


</script>

<template>
  <div class="media_expanded_wrapper">

    <div class="right">

      <img :src="data['poster_path']" class="poster" alt="poster" draggable="false">
      <expanded-header :data="data"></expanded-header>

    </div>

  </div>
</template>

<style scoped>
.media_expanded_wrapper {
  /*outline: 1px solid green;*/
  height: 100%;
  width: 100%;

  z-index: 2;
}

.right {
  height: 100%;
  /*width: 100%;*/
  display: flex;
  flex-flow: row nowrap;
}

.poster {
  height: 100%;
  margin: 0 auto 0 auto;
  max-height: 300px;
  /*outline: 1px solid red;*/
  border-radius: 10px;
  object-fit: contain;
  box-shadow: 3px 3px 2px #131215;
}

@media only screen and (max-width: 500px) {
  .right {
    flex-flow: column nowrap;
  }
  .poster {
    max-height: 400px;
    margin-bottom: 20px;
    width: 100%;
    object-fit: cover;
  }
}
</style>