<script setup>
import {computed, inject, onMounted, ref} from "vue";

import rating_info from '/home_images/rating_info.jpg'
import rating_arrows from '/home_images/rating_arrows.png'
import search_info from '/home_images/search_info.jpg'
import tags_info from '/home_images/tags_info.jpg'
import StatsGraphs from "@/components/General/StatsGraphs.vue";
import CreditsFooter from "@/components/General/CreditsFooter.vue";
import MediaScrollBanner from "@/components/MediaBanner/MediaScrollBanner.vue";
import MediaBanner from "@/components/MediaBanner/MediaBanner.vue";
import MovieContainer from '@/components/media_container/movie_container/MovieContainer.vue'

const curr_api = inject("curr_api");
const is_mobile = inject("is_mobile");

const default_movie = {
  "author": "David Ayer",
  "content_rating": {
    "id": 23,
    "name": "R",
    "order": 3
  },
  "created_at": "Tue, 31 Oct 2023 01:07:28 GMT",
  "episodes": null,
  "external_id": "228150",
  "external_link": "https://www.imdb.com/title/tt2713180",
  "external_name": "Fury",
  "genres": [
    {
      "id": 84,
      "name": "War",
      "origin": "movie"
    },
    {
      "id": 83,
      "name": "Drama",
      "origin": "movie"
    },
    {
      "id": 80,
      "name": "Action",
      "origin": "movie"
    }
  ],
  "id": 479,
  "is_deleted": null,
  "is_dropped": null,
  "media_medium": null,
  "media_type": "movie",
  "name": "Fury",
  "overview": "In the last months of World War II, as the Allies make their final push in the European theatre, a battle-hardened U.S. Army sergeant named 'Wardaddy' commands a Sherman tank called 'Fury' and its five-man crew on a deadly mission behind enemy lines. Outnumbered and outgunned, Wardaddy and his men face overwhelming odds in their heroic attempts to strike at the heart of Nazi Germany.",
  "poster_path": "https://image.tmdb.org/t/p/w500/pfte7wdMobMF4CVHuOxyu6oqeeA.jpg",
  "public_rating": 7.524,
  "release_date": "2014-10-15",
  "runtime": 135,
  "scaled_public_rating": 7.717795342875453,
  "seasons": null,
  "studio": "Columbia Pictures",
  "tags": [
    {
      "id": 28,
      "image_path": "203103-PLATINUM.png",
      "name": "Exciting",
      "origin": "movie",
      "overview": "Well crafted and engaging action",
      "tier": "green"
    },
    {
      "id": 16,
      "image_path": "101206-PLATINUM.png",
      "name": "Thrilling",
      "origin": "movie",
      "overview": "Will keep you on the edge of your seat",
      "tier": "green"
    }
  ],
  "themes": [],
  "tier_lists": [],
  "updated_at": "Thu, 25 Jan 2024 23:41:29 GMT",
  "user_rating": 8
}

onMounted(() => {
  window.scroll(0, 0)
})
</script>

<template>
  <div class="home_wrapper">

    <div class="intro_text">
      <h2>Welcome to Trusty's Corner !</h2>
      <p>This was made for fun while learning web-dev with the goal to more easily share my media recommendations with
        people.</p>
      <p>I also really love cataloguing.</p>
    </div>

    <media-scroll-banner></media-scroll-banner>

    <div class="intro_text" style="margin-top: 25px">
      <h1 style="margin-bottom: 20px">Watched recently</h1>
      <media-banner :order="'date_added'" :media_type="'movie'"></media-banner>
    </div>

    <div class="intro_text">
      <h1 style="margin-bottom: 20px">Latest release</h1>
      <media-banner :order="'release_date'" :media_type="'movie'"></media-banner>
    </div>

    <!--    <div class="intro_text">-->
<!--      <h1>Movie</h1>-->
<!--      <media-banner :media_type="'movie'" :ratings="[7,10]"></media-banner>-->
<!--    </div>-->

<!--    <div class="intro_text">-->
<!--      <h1>Show</h1>-->
<!--      <media-banner :media_type="'tv'" :ratings="[7,10]" :tier_lists="['not anime']"></media-banner>-->
<!--    </div>-->

    <div class="intro_text">
      <h1 style="font-size: 2em;text-decoration: underline">How does this work ?</h1>
    </div>
    <div class="intro_text">
      <h1>- Ratings</h1>
      <div>
        <p>Ratings are split into 3 components: my rating, the public rating and the combined rating circle.</p>
      </div>
      <div class="rating_example">
        <movie-container :data="default_movie" :scale_mul="!is_mobile ? 1.5 : 1"
        ></movie-container>
        <img :src="rating_arrows" alt="rating_info" class="rating_example_arrows">
      </div>
    </div>

    <div class="intro_text">
      <h1>- Tags</h1>
      <div>
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
      <img :src="tags_info" alt="search_info" class="home_image">
    </div>

    <div class="intro_text">
      <h1>- Searching</h1>
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

      <img :src="search_info" alt="search_info" class="home_image">
    </div>

    <div class="intro_text">
      <h1>- Stats for nerds (me)</h1>
    </div>

    <stats-graphs></stats-graphs>

    <credits-footer></credits-footer>

  </div>
</template>

<style scoped>
.home_wrapper {
  overflow: hidden;
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

.rating_example {
  /*outline: 1px solid red;*/
  margin-top: 30px;
  position: relative;
  display: flex;
  justify-content: center;
}

.rating_example_arrows {
  pointer-events: none;
  position: absolute;
  bottom: -70px;
  left: 55px;
  width: 800px;
  transform: translate(-20px);
  filter: drop-shadow(2px 2px 1px black) drop-shadow(1px 1px 3px black);
}

@media only screen and (max-width: 500px) {
  .home_wrapper {
    padding: 100px 20px 50px 20px;
  }

  .rating_example_arrows {
    bottom: -23px;
    left: -25px;
    width: 400px;
    /*transform: translate(-10px);*/
  }
}
</style>