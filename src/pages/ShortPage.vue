<script setup>
import {ref, onMounted, inject, provide, onUnmounted} from 'vue'
import MediaFeed from "@/components/media_feed/MediaFeed.vue";

</script>

<template>
  <media-feed :media_types="['movie']"
              :tier_lists="['short film']"
              :media_container_type="'movie'"
  ></media-feed>
</template>