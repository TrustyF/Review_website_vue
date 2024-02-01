<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "@/components/media_feed/MediaFeed.vue";

onMounted(() => {
  window.scroll(0, 0)
})
</script>

<template>
  <media-feed :media_type="'game'"
              :media_sizes="[[264,352],[264,352]]"
              :media_scales="[0.69,0.5]"
  ></media-feed>

</template>
