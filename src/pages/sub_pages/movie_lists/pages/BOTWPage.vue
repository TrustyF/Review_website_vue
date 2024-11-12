<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "../../../../components/media_feed/MediaFeed.vue";
import MediaFeedHeader from "@/components/media_feed/MediaFeedHeader.vue";

onMounted(() => {
  window.scroll(0, 0)
})
</script>

<template>
  <media-feed-header
      title="Best of the worst"
      desc="A list of extremely entertaining bad movies"
  />
  <media-feed :media_types="['movie']"
              :tier_lists="['best of the worst']"
              :media_container_type="'movie'"
              :group_rating="false"
  ></media-feed>
</template>