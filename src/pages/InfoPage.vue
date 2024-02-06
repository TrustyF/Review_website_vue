<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MovieContainer from '@/components/media_container/movie_container/MovieContainer.vue'
import rating_arrows from '/home_images/rating_arrows.png'
import CreditsFooter from "@/components/General/CreditsFooter.vue";
import StatsGraphs from '@/components/General/StatsGraphs.vue'

import ratings_info from '/home_images/rating_info.jpg'
import tags_info from '/home_images/tags_info.jpg'
import search_info from '/home_images/search_info.jpg'


let props = defineProps(["test"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");
const is_mobile = inject("is_mobile");

</script>

<template>
  <div class="info_wrapper">

    <h1>How does this work ?</h1>

    <div class="text_block">
      <h1>Ratings</h1>
      <p>Ratings are split into: my personal rating, public rating and the combined circle.</p>
    </div>

    <img :src="ratings_info" alt="search_info" class="image_block">

    <div class="text_block">
      <p>The public rating is visually remapped to better match my personal rating distribution.</p>
      <br>
      <p>The combined circle takes the average of both ratings to provide an easy shorthand of the overall consensus
        between my personal assessment and the public opinion but also serves as a valuable reference for
        decision-making.</p>
      <br>
      <p>This collaborative approach ensures a more comprehensive and balanced evaluation, taking into
        account both personal preference and the collective sentiment</p>
    </div>


    <div class="text_block">
      <h1>Tags</h1>
      <p>Medias are annotated with various tags. These are meant to provide a simple breakdown of my opinion,
        and to help you decide what to pick. Tags are categorized into different colors representing their
        sentiment:</p>

      <div
          style="display: grid;grid-template-columns: fit-content(100%) 1fr;column-gap: 10px;align-items: flex-start;margin: 10px">

        <p style="margin-left: 20px;color: #dcc14d">Gold</p>
        <p>: the highest honors, the best at what it does</p>
        <p style="margin-left: 20px;color: #529a2e">Green</p>
        <p>: Positive</p>
        <p style="margin-left: 20px;color: #ce17ca">Purple</p>
        <p>: Caveat or disclaimer</p>
        <p style="margin-left: 20px;color: #b42121">Red</p>
        <p>: Negative</p>
        <p style="margin-left: 20px;color: #667581">Grey</p>

        <p>: Gripe or light criticism</p>
      </div>

    </div>
    <img :src="tags_info" alt="search_info" class="image_block">

    <div class="text_block">
      <h1>Searching</h1>
      <div>
        <p>The search bar can search for many different fields including:</p>
        <p style="margin-left: 20px"> - name<br>
          - genre<br>
          - tags<br>
          - studio<br>
          - author
        </p>
      </div>
      <p>Filters can also be found next to the search bar and are applied additively.</p>

    </div>
    <img :src="search_info" alt="search_info" class="image_block">


    <div class="text_block">
      <h1>Stats for nerds (me)</h1>
    </div>

    <stats-graphs></stats-graphs>

    <credits-footer></credits-footer>

  </div>
</template>

<style scoped>
.info_wrapper {

  display: flex;
  flex-flow: column;
  gap: 20px;
  margin: 0 auto 0 auto;
  padding: 120px 0 100px 0;
  position: relative;
  min-height: 80vh;
}

.text_block {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
  font-size: 1em;
  line-height: 1.5;
  word-wrap: break-word;
  font-weight: 400;
}

h1 {
  font-size: 1.5em;
  font-weight: 600;
  margin-bottom: 15px;
  text-decoration: 0.025em #575757 underline;
  text-underline-offset: 4px;
}

p {
  font-size: 1em;
  color: #d2d2d2;
}

.image_block {
  /*outline: 1px solid red;*/
  /*height: 200px;*/
  object-fit: contain;
  border: 2px solid #464646;
  border-radius: 20px;
  filter: drop-shadow(2px 2px 3px black) drop-shadow(2px 2px 2px black);
}
</style>