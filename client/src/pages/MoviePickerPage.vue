<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaList from "@/components/MediaContainer/List/MediaList.vue";
import MediaPane from "@/components/MediaContainer/Pane/MediaPane.vue";

</script>

<template>
  <media-list media_type="movie"></media-list>
</template>
