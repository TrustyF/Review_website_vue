<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "../../../components/media_feed/MediaFeed.vue";

onMounted(() => {
  window.scroll(0, 0)
})
</script>

<template>
  <media-feed :media_type="'youtube'"
              :tier_lists="['animation']"
              :media_sizes="[[1280,720],[1280,720]]"
              :media_scales="[0.2,0.14]"
  ></media-feed>
</template>