<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaList from "@/components/MediaContainer/MediaList.vue";
import MediaPane from "@/components/MediaPane/MediaPane.vue";

</script>

<template>
  <media-pane></media-pane>
  <media-list media_type="game"></media-list>
</template>