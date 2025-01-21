<script setup>
import {ref, onMounted, inject, provide, defineAsyncComponent} from 'vue'
const MediaFeed = defineAsyncComponent(() => import('@/components/media_feed/MediaFeed.vue'));

</script>

<template>
  <media-feed :media_types="['game']"
              :media_container_type="'game'"
  ></media-feed>

</template>
