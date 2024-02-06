<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "@/components/media_feed/MediaFeed.vue";

onMounted(() => {
  window.scroll(0, 0)
})
</script>

<template>
  <media-feed :media_types="['tv']"
              :tier_lists="['not anime']"
              :media_container_type="'tv'"
  ></media-feed>

</template>
