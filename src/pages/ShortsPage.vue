<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "@/components/media_feed/MediaFeed.vue";

</script>

<template>
  <media-feed :media_type="'short'"
              :media_sizes="[[480,240],[480,240]]"
              :media_scales="[0.75,0.4]"
  ></media-feed>
</template>
