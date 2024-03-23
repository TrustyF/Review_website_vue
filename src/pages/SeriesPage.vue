<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "@/components/media_feed/MediaFeed.vue";


</script>

<template>
  <media-feed :media_types="['tv']"
              :media_container_type="'tv'"
  ></media-feed>

</template>
