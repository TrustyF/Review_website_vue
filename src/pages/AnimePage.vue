<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "@/components/media_feed/MediaFeed.vue";

</script>

<template>
  <media-feed :media_type="'anime'"
              :media_sizes="[[500,750],[500,750]]"
              :media_scales="[0.35,0.2]"
  ></media-feed>

</template>
