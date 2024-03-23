<script setup>
import {computed, inject, onMounted, ref} from "vue";

import CreditsFooter from "@/components/General/CreditsFooter.vue";
import MediaScrollBanner from "@/components/MediaBanner/MediaScrollBanner.vue";
import MediaBanner from "@/components/MediaBanner/MediaBanner.vue";
import logo from '/ui/logo.png'
import {RouterLink} from "vue-router";

const curr_api = inject("curr_api");
const is_mobile = inject("is_mobile");


onMounted(() => {
  window.scroll(0, 0)
})
</script>

<template>
  <div class="home_wrapper">

    <div class="top_banner"
         style="position: relative;padding:20px;border-radius:10px;display: flex;justify-content: center">
      <img
          style="width: 150px;border-radius: 10px;object-fit: contain;margin-right: auto;background-color: #36204a;
          filter:drop-shadow(5px 5px 10px black)"
          :src="logo" alt="logo">
      <h2 style="font-size: 2em;
      filter:drop-shadow(3px 3px 2px black)drop-shadow(1px 1px 8px black)drop-shadow(1px 1px 15px black)">
        Welcome to Trusty's Corner !</h2>
      <RouterLink style="color: grey;filter:drop-shadow(2px 2px 2px black);text-underline-offset: 2px;margin: -10px 0 -20px 10px;font-size: 1em" to="/info">What is this ?</RouterLink>

      <media-scroll-banner></media-scroll-banner>
    </div>

    <div class="" style="margin-top: 5px">
      <h1>Watched recently</h1>
      <div style="margin: 10px 0 20px 0" class="separator"></div>
      <media-banner :order="'date_added'" :media_types="['movie','tv']"></media-banner>
    </div>

    <div class="">
      <h1>Latest releases</h1>
      <div style="margin: 10px 0 20px 0" class="separator"></div>
      <media-banner :order="'release_date'" :media_types="['movie','tv']"></media-banner>
    </div>

    <div class="">
      <h1>Recommended movie</h1>
      <div style="margin: 10px 0 20px 0" class="separator"></div>
      <media-banner :ratings=[7,10] :media_types="['movie']"></media-banner>
    </div>

    <div class="">
      <h1>Recommended manga</h1>
      <div style="margin: 10px 0 20px 0" class="separator"></div>
      <media-banner :ratings=[7,10] :media_types="['manga']" :size_override="[512, 720]"></media-banner>
    </div>

    <div class="">
      <h1>Recommended games</h1>
      <div style="margin: 10px 0 20px 0" class="separator"></div>
      <media-banner :ratings=[7,10] :media_types="['game']" :size_override="[528, 704]"></media-banner>
    </div>

    <credits-footer></credits-footer>

  </div>
</template>

<style scoped>
.home_wrapper {
  display: flex;
  flex-flow: column;
  gap: 40px;
  margin: 0 auto 0 auto;
  padding: 120px 0 100px 0;
  position: relative;
  /*outline: 1px solid red;*/
  min-height: 80vh;
  /*background-color: #1c1b23;*/
}
.separator {
  height: 1px;
  background-color: #2b2a34;
}

.top_banner {
  display: flex;
  flex-flow: column;
  gap: 20px;
}

@media only screen and (max-width: 500px) {
  .top_banner {
    margin-top: 20px;
  }
  .home_wrapper {
    padding: 100px 20px 50px 20px;
  }
}
</style>