<script setup>
import {ref, onMounted, inject} from 'vue'
import MediaList from "@/components/MediaContainer/MediaList.vue";

const mediaType = ref("movie")
</script>

<template>
  <media-list media_type="movie"></media-list>
</template>
