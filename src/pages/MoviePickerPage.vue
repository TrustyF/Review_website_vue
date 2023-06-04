<script setup>
import {ref, onMounted, onUnmounted, inject} from 'vue'
import RandomGenreBanner from '@/components/Media/banners/RandomGenreBanner'
import FilterMenu from "@/components/Media/general/FilterMenu";

</script>

<template>
  <div class="pick_page_feed_wrapper">
    <div>
      <h1 class="headers"> What are you in the mood for ?</h1>
      <RandomGenreBanner mediaType="movie" banner-type="random_genre"></RandomGenreBanner>
    </div>
    <div>
      <h1 class="headers">How about a recent release.</h1>
      <RandomGenreBanner mediaType="movie" banner-type="recent_release"></RandomGenreBanner>
    </div>
    <div>
      <h1 class="headers">Longer form content perhaps ?</h1>
      <RandomGenreBanner mediaType="tv" banner-type="random_genre"></RandomGenreBanner>
    </div>
    <div>
      <h1 class="headers">Looking for a good read ?</h1>
      <RandomGenreBanner mediaType="manga" banner-type="random_genre"></RandomGenreBanner>
    </div>
  </div>
</template>

<script>

</script>

<style scoped>
.pick_page_feed_wrapper {
  padding: 30px 0 30px 0;
  /*width: 80%;*/
  margin: auto;
  display: flex;
  flex-flow: column;
  gap: 50px;
}

.headers {
  font-weight: bold;
  font-size: 1.2em;
  margin: 0 0 20px 10%;
}
</style>