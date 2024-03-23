<script setup>
import {ref, onMounted, inject, provide, onUnmounted} from 'vue'
import MediaFeed from "@/components/media_feed/MediaFeed.vue";

</script>

<template>
  <media-feed :media_types="['manga']"
              :media_container_type="'manga'"></media-feed>
</template>
