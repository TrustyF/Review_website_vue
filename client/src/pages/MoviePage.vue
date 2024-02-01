<script setup>
import {ref, onMounted, inject, provide, onUnmounted} from 'vue'
import MediaFeed from "@/components/media_feed/MediaFeed.vue";

onMounted(() => {
  window.scroll(0, 0)
})
</script>

<template>
  <media-feed media_type="movie"
  ></media-feed>
</template>