<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaBanner from "../../../components/MediaBanner/MediaBanner.vue";

let props = defineProps({
  test: {
    type: String,
    default: null,
  },
});
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="banner" style="min-height: 341px;margin-top: 100px;">
    <media-banner :ratings=[7,10]
                  :media_types="['movie']"></media-banner>
  </div>
</template>

<style scoped>

</style>