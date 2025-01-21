<script setup>
import {ref, onMounted, inject, provide, onUnmounted, defineAsyncComponent} from 'vue'
const MediaFeed = defineAsyncComponent(() => import('@/components/media_feed/MediaFeed.vue'));

</script>

<template>
  <media-feed :media_types="['movie']"
              :media_container_type="'movie'"></media-feed>
</template>