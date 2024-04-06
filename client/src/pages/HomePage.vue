<script setup>
import {computed,defineAsyncComponent, inject, onBeforeMount, onMounted, onUnmounted, ref} from "vue";

import CreditsFooter from "../components/General/CreditsFooter.vue";
import MediaScrollBanner from "../components/MediaBanner/MediaScrollBanner.vue";
import MediaBanner from "../components/MediaBanner/MediaBanner.vue";
import logo from '/ui/logo.png'
import {RouterLink} from "vue-router";

const curr_api = inject("curr_api");
const is_mobile = inject("is_mobile");

const load_number = ref(-1)

const genre_number_list = [
    ['Action',80],
    ['Adventure',79],
    ['Sci-Fi',78],
    ['Mystery',92],
    ['Crime',85],
    ['Animation',88],
    ['Horror',89],
    ['Comedy',87],
    ['Romance',90],
]

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

    <div class="banner" style="margin-top: 5px">
      <h1>Watched recently</h1>
      <media-banner :order="'date_added'" :media_types="['movie','tv']" v-if="load_number>=-1" @loaded="load_number+=1"></media-banner>
    </div>

    <div class="banner">
      <h1>Latest releases</h1>
      <media-banner :order="'release_date'" :media_types="['movie','tv']" v-if="load_number>=0" @loaded="load_number+=1"></media-banner>
    </div>

    <div class="banner">
      <h1>Movies</h1>
      <media-banner :ratings=[7,10] :media_types="['movie']" v-if="load_number>=1" @loaded="load_number+=1"></media-banner>
    </div>

    <div class="banner">
      <h1>Manga</h1>
      <media-banner :ratings=[7,10] :media_types="['manga']" :size_override="[512, 720]" v-if="load_number>=2" @loaded="load_number+=1"></media-banner>
    </div>

    <div class="banner">
      <h1>Games</h1>
      <media-banner :ratings=[7,10] :media_types="['game']" :size_override="[528, 704]" v-if="load_number>=3" @loaded="load_number+=1"></media-banner>
    </div>

    <div class="banner">
      <h1>Youtube shows</h1>
      <media-banner :ratings=[7,10] :media_types="['youtube']" :tier_lists="['tv-show']" :limit="10" :size_override="[910, 512]" v-if="load_number>=4" @loaded="load_number+=1"></media-banner>
    </div>

    <div class="banner">
      <h1>Youtube documentaries</h1>
      <media-banner :ratings=[7,10] :media_types="['youtube']" :tier_lists="['documentary']" :limit="10" :size_override="[910, 512]" v-if="load_number>=5" @loaded="load_number+=1"></media-banner>
    </div>

    <div class="banner">
      <h1>Youtube essays</h1>
      <media-banner :ratings=[7,10] :media_types="['youtube']" :tier_lists="['essay']" :limit="10" :size_override="[910, 512]" v-if="load_number>=6" @loaded="load_number+=1"></media-banner>
    </div>

    <div class="banner" v-for="(entry,index) in genre_number_list" :key="entry[1]">
      <h1>{{entry[0]}}</h1>
      <media-banner :ratings=[6,10] :media_types="['movie']" :genres="[entry[1]]" v-if="load_number>=6+index" @loaded="load_number+=1"></media-banner>
    </div>


    <div class="banner">
      <h1>Wall of shame</h1>
      <media-banner :ratings=[1,4] :media_types="['movie','tv']" :limit="20" v-if="load_number>=16" @loaded="load_number+=1"></media-banner>
    </div>

    <credits-footer></credits-footer>

  </div>
</template>

<style scoped>
h1 {
  margin: 0 0 20px 0
}
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
.banner {
  /*outline: 1px solid red;*/
  min-height: 341px;
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