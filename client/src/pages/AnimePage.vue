<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaList from "@/components/MediaContainer/Master/MediaList.vue";
import MediaPane from "@/components/MediaContainer/Pane/MediaPane.vue";

</script>

<template>
  <media-pane></media-pane>
  <media-list media_type="anime"></media-list>
</template>