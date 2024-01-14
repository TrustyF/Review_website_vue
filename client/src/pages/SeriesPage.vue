<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "@/components_V2/media_feed/MediaFeed.vue";

</script>

<template>
  <media-feed :media_type="'tv'"
              :media_size="[500,750]"
              :media_scale="[0.35,0.19]"
  ></media-feed>

</template>
