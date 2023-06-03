<script setup>
import {ref, onMounted, onUnmounted, inject} from 'vue'
import RandomGenreBanner from '@/components/Media/banners/RandomGenreBanner'
import FilterMenu from "@/components/Media/general/FilterMenu";

</script>

<template>
  <div class="pick_page_feed_wrapper">
    <h1 style="font-weight: bold;font-size: 1.2em;padding: 10px">What are you in the mood for ?</h1>
    <RandomGenreBanner mediaType="movie"></RandomGenreBanner>
  </div>
</template>

<script>

</script>

<style scoped>
.pick_page_feed_wrapper {
  padding: 10px;
  /*outline: 1px red solid;*/
  width: 80%;
  margin: auto;
}
</style>