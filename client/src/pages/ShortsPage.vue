<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "@/components_V2/media_feed/MediaFeed.vue";

</script>

<template>
  <media-feed :media_type="'short'"
              :media_size="[[480,240],[480,240]]"
              :media_scale="[0.75,0.4]"
  ></media-feed>
</template>
