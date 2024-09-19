<script setup>
import {computed, defineAsyncComponent, inject, onBeforeMount, onMounted, onUnmounted, ref} from "vue";

import CreditsFooter from "../components/General/CreditsFooter.vue";
import MediaScrollBanner from "../components/MediaBanner/MediaScrollBanner.vue";
import MediaBanner from "../components/MediaBanner/MediaBanner.vue";
import logo from '/ui/logo.png'
import {RouterLink} from "vue-router";

const curr_api = inject("curr_api");
const is_mobile = inject("is_mobile");

const load_number = ref(-1)

const genre_number_list = [
  ['Action', 80],
  ['Adventure', 79],
  ['Sci-Fi', 78],
  ['Mystery', 92],
  ['Crime', 85],
  ['Animation', 88],
  ['Horror', 89],
  ['Comedy', 87],
  ['Romance', 90],
]

</script>

<template>
  <div class="home_wrapper">

    <media-scroll-banner></media-scroll-banner>

    <div class="top_banner"
         style="position: relative;padding:20px;border-radius:10px;display: flex;justify-content: center">
      <img
          style="width: 150px;border-radius: 10px;object-fit: contain;margin-right: auto;background-color: #36204a;
          filter:drop-shadow(5px 5px 10px black)"
          :src="logo" alt="logo">

      <h2 style="font-size: 2em;
      filter:drop-shadow(3px 3px 2px black)drop-shadow(1px 1px 8px black)drop-shadow(1px 1px 15px black)">
        Welcome to Trusty's Corner !</h2>

      <RouterLink class="whats_this" to="/info">What is this ?
      </RouterLink>
    </div>


    <lazy-component class="banner">
      <media-banner :ratings=[7,10]
                    title="Recommended movies"
                    :media_types="['movie']"
      ></media-banner>
    </lazy-component>

    <lazy-component class="banner">
      <media-banner :order="'date_added'"
                    title="Watched recently"
                    :media_types="['movie','tv']"
      ></media-banner>
    </lazy-component>

    <lazy-component class="banner">
      <media-banner :order="'release_date'"
                    title="Latest releases"
                    :media_types="['movie','tv']"
      ></media-banner>
    </lazy-component>

    <lazy-component class="banner">
      <media-banner :ratings=[6,10]
                    title="TV"
                    :media_types="['Tv']"
                    :size_override="[512, 720]"
      ></media-banner>
    </lazy-component>

    <lazy-component class="banner" v-for="(entry) in genre_number_list" :key="entry[1]">
      <media-banner :ratings=[6,10]
                    :title="entry[0]"
                    :media_types="['movie']"
                    :genres="[entry[1]]"
      ></media-banner>
    </lazy-component>

    <lazy-component class="banner">
      <media-banner :ratings=[7,10]
                    title="Manga"
                    :media_types="['manga']"
                    :size_override="[512, 720]"></media-banner>
    </lazy-component>

    <lazy-component class="banner">
      <media-banner :ratings=[7,10]
                    title="Read recently"
                    :order="'date_added'"
                    :media_types="['manga']"
                    :size_override="[512, 720]"></media-banner>
    </lazy-component>

    <lazy-component class="banner">
      <media-banner :ratings=[7,10]
                    title="Games"
                    :media_types="['game']"
                    :size_override="[528, 704]"></media-banner>
    </lazy-component>

    <lazy-component class="banner">
      <media-banner :ratings=[7,10]
                    title="Played recently"
                    :order="'date_added'"
                    :media_types="['game']"
                    :size_override="[528, 704]"></media-banner>
    </lazy-component>

    <lazy-component class="banner">
      <media-banner :ratings=[7,10]
                    title="Youtube shows"
                    :media_types="['youtube']"
                    :tier_lists="['tv-show']"
                    :limit="10"
                    :size_override="[910, 512]"></media-banner>
    </lazy-component>

    <lazy-component class="banner">
      <media-banner :ratings=[7,10]
                    title="Youtube documentaries"
                    :media_types="['youtube']"
                    :tier_lists="['documentary']"
                    :limit="10"
                    :size_override="[910, 512]"></media-banner>
    </lazy-component>

    <lazy-component class="banner">
      <media-banner :ratings=[7,10]
                    title="Youtube essays"
                    :media_types="['youtube']"
                    :tier_lists="['essay']"
                    :limit="10"
                    :size_override="[910, 512]"></media-banner>
    </lazy-component>

    <lazy-component class="banner">
      <media-banner :ratings=[1,4]
                    title="Wall of shame"
                    :media_types="['movie','tv']"
                    :limit="20"></media-banner>
    </lazy-component>

    <credits-footer></credits-footer>

  </div>
</template>

<style scoped>

.home_wrapper {
  display: flex;
  flex-flow: column;
  gap: 20px;
  margin: 0 auto 0 auto;
  padding: 120px 0 100px 0;
  position: relative;
  min-height: 80vh;
  /*background-color: #1c1b23;*/
  /*outline: 1px solid red;*/
}

.banner {
  /*outline: 1px solid red;*/
  min-height: 340px;
}
.whats_this {
  color: #969696;
  filter: drop-shadow(2px 2px 2px #464646);
  text-decoration: none;
  border: 1px solid #5b5b5b;
  font-size: 1em;
  border-radius: 8px;
  padding: 5px;
  margin-top: 5px;
  transition: 100ms ease;
  backdrop-filter: blur(5px);
}

.whats_this:hover {
  background-color: #969696;
  color: black;
}
.top_banner {
  /*outline: 1px solid red;*/
  display: flex;
  flex-flow: column;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 30px;
}

@media only screen and (max-width: 500px) {
  .home_wrapper {
    gap: 10px;
  }

  .top_banner {
    /*margin-top: 20px;*/
  }

  .banner {
    min-height: 295px;
  }

  .home_wrapper {
    padding: 100px 20px 50px 20px;
  }
}
</style>