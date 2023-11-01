<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaList from "@/components/MediaContainer/MediaList.vue";
import MediaPane from "@/components/MediaPane/MediaPane.vue";

const mediaType = ref("movie")
const selected_media = ref(undefined)

provide('selected_media', selected_media)

</script>

<template>
  <media-pane></media-pane>
  <media-list media_type="movie"></media-list>

</template>
