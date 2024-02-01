<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "../../../components/media_feed/MediaFeed.vue";

onMounted(() => {
  window.scroll(0, 0)
})
</script>

<template>
  <media-feed :media_type="'youtube'"
              :tier_lists="['short film']"
  ></media-feed>
</template>