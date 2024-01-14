<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "@/components_V2/media_feed/MediaFeed.vue";

</script>

<template>
  <media-feed :media_type="'game'"
              :media_sizes="[[264,352],[264,352]]"
              :media_scales="[0.69,0.36]"
  ></media-feed>

</template>
