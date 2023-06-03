<script setup>
import {ref, onMounted, onUnmounted, inject} from 'vue'
import RandomGenreBanner from '@/components/Media/banners/RandomGenreBanner'
import FilterMenu from "@/components/Media/general/FilterMenu";
import RecentReleaseBanner from "@/components/Media/banners/RecentReleaseBanner";


let num_media_fit = ref(0)

function calc_screen_fit() {
  let feed_width = window.outerWidth * 0.8
  let media_width = 200
  let gap = 25
  let padding = 40

  num_media_fit.value = Math.floor((feed_width - (padding * 2)) / (media_width + gap))
  console.log(num_media_fit.value)
}

onMounted(() => {
  calc_screen_fit()
  addEventListener('resize', calc_screen_fit)
})
onUnmounted(() => {
  removeEventListener('resize', calc_screen_fit)
})
</script>

<template>
  <div class="pick_page_feed_wrapper">
    <div>
      <h1 class="headers"> What are you in the mood for ?</h1>
      <RandomGenreBanner mediaType="movie" :max_media="num_media_fit"></RandomGenreBanner>
    </div>
    <div>
      <h1 class="headers">How about a recent release.</h1>
      <RecentReleaseBanner mediaType="movie" :max_media="num_media_fit"></RecentReleaseBanner>
    </div>
    <div>
      <h1 class="headers">Longer form content perhaps ?</h1>
      <RandomGenreBanner mediaType="tv" :max_media="num_media_fit"></RandomGenreBanner>
    </div>
    <div>
      <h1 class="headers">Looking for a good read ?</h1>
      <RandomGenreBanner mediaType="manga" :max_media="num_media_fit"></RandomGenreBanner>
    </div>
  </div>
</template>

<script>

</script>

<style scoped>
.pick_page_feed_wrapper {
  padding: 30px 0 30px 0;
  /*outline: 1px red solid;*/
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