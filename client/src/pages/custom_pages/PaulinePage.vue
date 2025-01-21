<script setup>
import {ref, onMounted, inject, provide, onUnmounted,defineAsyncComponent} from 'vue'
const MediaFeed = defineAsyncComponent(() => import('@/components/media_feed/MediaFeed.vue'));

</script>

<template>
  <media-feed :user_lists="['pauline']"
              :tier_lists="['all']"
              :media_container_type="'movie'"
              :group_rating="false"
  ></media-feed>
</template>