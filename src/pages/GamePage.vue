<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "@/components/media_feed/MediaFeed.vue";


</script>

<template>
  <media-feed :media_types="['game']"
              :media_container_type="'game'"
  ></media-feed>

</template>
