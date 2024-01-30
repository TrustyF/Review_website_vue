<script setup>
import {computed, inject, onMounted, ref} from "vue";

import rating_info from '/home_images/rating_info.jpg'
import search_info from '/home_images/search_info.jpg'
import tags_info from '/home_images/tags_info.jpg'
import StatsGraphs from "@/components/General/StatsGraphs.vue";
import CreditsFooter from "@/components/General/CreditsFooter.vue";

const curr_api = inject("curr_api");

</script>

<template>
  <div class="home_wrapper">

    <div class="intro_text">
      <h2>Welcome to Trusty's Corner !</h2>
      <p>This was made for fun while learning web-dev with the goal to more easily share my media recommendations with
        people.</p>
      <p>I also really love cataloguing.</p>
    </div>

    <div class="intro_text">
      <h1>Ratings</h1>
      <div>
        <p>Ratings are split into 3 components: my rating, the public rating and the combined rating circle.</p>
      </div>
      <img :src="rating_info" alt="rating_info" class="home_image">
    </div>

    <div class="intro_text">
      <h1>Tags</h1>
      <div>
        <p>Medias are annotated with various tags. These are meant to provide a simple breakdown of my opinion,
          and to help you decide what to pick. Tags are categorized into different colors representing their
          sentiment:</p>
        <p style="margin-left: 20px"> - Gold: the highest honors, the best at what it does</p>
        <p style="margin-left: 20px"> - Green: Positive</p>
        <p style="margin-left: 20px"> - Purple: Caveat or disclaimer</p>
        <p style="margin-left: 20px"> - Red: Negative</p>
        <p style="margin-left: 20px"> - Grey: Gripe or light criticism</p>
      </div>
      <img :src="tags_info" alt="search_info" class="home_image">
    </div>

    <div class="intro_text">
      <h1>Searching</h1>
      <div>
        <p>The search bar can search for many different fields including:</p>
        <p style="margin-left: 20px"> - approximate name<br>
          - genre<br>
          - tags<br>
          - studio<br>
          - author
        </p>
      </div>
      <p>Filters can also be found next to the search bar and are applied additively.</p>

      <img :src="search_info" alt="search_info" class="home_image">
    </div>

    <div class="intro_text">
      <h1>Stats for nerds (me)</h1>
    </div>

    <stats-graphs></stats-graphs>

    <credits-footer></credits-footer>

  </div>
</template>

<style scoped>
.home_wrapper {
  display: flex;
  flex-flow: column;
  gap: 40px;
  margin: 0 auto 0 auto;
  padding: 120px 150px 100px 150px;
  position: relative;
  /*outline: 1px solid red;*/
  min-height: 80vh;
  /*background-color: #1c1b23;*/
}

.intro_text {
  display: flex;
  flex-flow: column;
  gap: 10px;
  /*outline: 1px solid grey;*/
}

.intro_text h2 {
  font-size: 2em;
  font-weight: 1000;
}

.intro_text h1 {
  font-size: 1.5em;
  /*text-decoration: underline;*/
  font-weight: 800;
}

.intro_text p {
  font-size: 0.9em;
  font-weight: 300;
  line-height: 1.5em;
  color: #969696;
  font-family: sans-serif;
  /*margin-left: 20px;*/
}

.home_image {
  /*outline: 1px solid red;*/
  /*height: 200px;*/
  object-fit: contain;
  border: 2px solid #464646;
  border-radius: 20px;
  filter: drop-shadow(2px 2px 3px black) drop-shadow(2px 2px 2px black);
}



@media only screen and (max-width: 500px) {
  .home_wrapper {
    padding: 100px 20px 50px 20px;
  }
}
</style>