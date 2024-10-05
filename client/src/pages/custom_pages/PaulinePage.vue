<script setup>
import {ref, onMounted, inject, provide, onUnmounted} from 'vue'
import MediaFeed from "@/components/media_feed/MediaFeed.vue";

</script>

<template>
  <media-feed :tier_lists="['pauline']"
              :media_container_type="'movie'"
  ></media-feed>
</template>