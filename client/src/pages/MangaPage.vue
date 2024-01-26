<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "@/components/media_feed/MediaFeed.vue";

</script>

<template>
  <media-feed :media_type="'manga'"
              :media_sizes="[[256,360],[256,360]]"
              :media_scales="[0.7,0.5]"
  ></media-feed>
</template>
