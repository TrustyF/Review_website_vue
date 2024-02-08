<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "@/components/media_feed/MediaFeed.vue";

onMounted(() => {
  window.scroll(0, 0)
})
</script>

<template>
  <media-feed :media_types="['movie','tv']"
              :tier_lists="['anime']"
              :media_container_type="'movie'"
  ></media-feed>

</template>
