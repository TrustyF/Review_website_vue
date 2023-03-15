<script setup>
import TagContainer from "./TagContainer";
import {clickOutSide as vClickOutSide} from '@mahdikhashan/vue3-click-outside'
import DbHelper from "@/components/DbHelper";
</script>

<template>
  <!--  <db-helper :open="settingsOpen" :input-data="data"></db-helper>-->
  <div class="movie_container" :class="[isOpen ? 'open' : 'closed'] + [isSeen ? ' seen' : '']">
    <div class="main_block">

      <div class="settings">
        <button @click="settingsOpen = !settingsOpen">...</button>
      </div>

      <!--      <div class="tags_list_poster">-->
      <!--        <tag-container v-for="tag in data['tags']" :key="tag" :tag="tag"/>-->
      <!--      </div>-->

      <img v-lazy="`https://image.tmdb.org/t/p/w500${data['poster_path']}`" class="poster" alt="poster"
           v-click-out-side="clickOutside"
           @click="isOpen = !isOpen">

      <div class="content" @click="isSeen = !isSeen">
        <p class="title">{{ data['title'] }}</p>
        <p class="date" v-if="data['release_date']">{{ data['release_date'].split("-")[0] }}</p>
        <p class="rating">{{ data['my_rating'] + "★" }} </p>
      </div>


    </div>

    <div class="expanded">
      <div class="overview">

        <h3 class="heading">Overview</h3>
        <div class="details_wrapper">
          <p class="rank" v-if="data['genres']" style="margin-bottom:5px;">
            {{ data['genres'].map(elem => elem).join(', ') }}</p>
          <p class="rank" style="margin-bottom:5px;"> {{ "Duration: " + timeConvert(data['runtime']) }}</p>
          <p class="rank" v-if="data['contentRating']">{{ "Rating: " + data['contentRating'] }}</p>

          <h3 class="heading">Public reception</h3>
          <p class="rank" v-if="data['vote_average']">{{ Math.round(data['vote_average'] * 10) / 10 }}/10</p>
          <!--          <round-progress-classic :data="data['rating']['ratingValue']" :number="true"></round-progress-classic>-->
          <h3 class="heading">Extras</h3>
          <a :href="data['imdb_url']" target="_blank" rel="noopener noreferrer">
            <button type="button"
                    style="background-color: #F5C518;border-radius: 3px;padding: 3px;outline: 1px black solid;border-style: none;cursor:pointer ">
              Imdb
            </button>
          </a>
        </div>
      </div>
    </div>

    <div class="seen_block"><div class="checkmark"></div></div>
  </div>
</template>


<script>
export default {
  name: "MovieContainer",
  props: {
    data: Object,
  },
  data() {
    return {
      isOpen: false,
      isSeen: false,
      outOfFocus: false,
      settingsOpen: false
    }
  },
  mounted() {
    // console.log(`${this.data['name']} is mounted!`)
  },
  methods: {
    timeConvert(n) {
      const hours = (n / 60);
      const rhours = Math.floor(hours);
      const minutes = (hours - rhours) * 60;
      const rminutes = Math.round(minutes);
      return rhours + " h " + rminutes + " minutes";
    },
    clickOutside(input) {
      this.isOpen = false
    },
  }
}
</script>
<style scoped>
.movie_container {
  /*outline: 1px solid green;*/

  background-color: white;

  width: 200px;
  /*height: 355px;*/
  /*max-width: 400px;*/
  /*min-width: 200px;*/

  margin: 15px;
  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);

  overflow: hidden;
  transition: 0.2s ease;

  display: flex;

}

.settings {
  position: absolute;
}

.main_block {
  /*outline: 2px solid yellow;*/
  width: 200px;
  display: block;
}

.expanded {
  /*outline: 1px red solid;*/
  border-radius: 8px 8px 0 0;

  padding: 20px 20px 20px 20px;
  position: absolute;

  width: 160px;
  height: 260px;

  background-color: rgba(255, 255, 255, 0.85);

  font-size: 0.7em;
  text-align: left;

  visibility: hidden;
  opacity: 0;
  transition: all 0.2s;
}

.open .expanded {
  visibility: visible;
  opacity: 1;
}

.seen_block {
  /*outline: 1px red solid;*/
  border-radius: 8px 8px 0 0;

  padding: 20px 20px 20px 20px;
  position: absolute;

  width: 160px;
  height: 260px;

  background-color: rgba(0, 0, 0, 0.75);

  visibility: hidden;
  opacity: 0;
  transition: all 0.2s;
}

.checkmark {
  display: inline-block;
  transform: rotate(45deg);
  height: 25px;
  width: 12px;
  margin-left: 90%;
  margin-top: -10%;
  border-bottom: 7px solid rgba(173, 255, 47,1);
  border-right: 7px solid rgba(173, 255, 47,1);
}

.seen .seen_block {
  visibility: visible;
  opacity: 1;
}

.heading {
  /*padding: 10px 0 5px 0 ;*/
  line-height: 25px;
  text-decoration: underline;
}

.poster {
  border-radius: 8px 8px 0 0;
  width: 200px;
  aspect-ratio: 1/1.5;
}

.content {
  /*outline: 1px solid red;*/
  display: grid;
  justify-content: space-between;
  flex-direction: column;

  margin: 5px 10px 10px 10px;
}

.extra_content {
  position: absolute;
  transform: translate(0px, 280px);
}

.title {
  /*outline: 1px solid red;*/
  font-size: 0.8em;
  text-align: left;
  margin: 0;
  /*overflow: hidden;*/
  white-space: nowrap;
}

.date, .rating {
  /*outline: 1px solid red;*/

  font-size: 0.7em;
  text-align: left;
  margin: 0;

  color: rgba(0, 0, 0, 0.6);

  /*overflow-wrap: normal;*/
}

.overview {
}

.genres {
  /*outline: 1px red solid;*/
  display: flex;
  flex-wrap: nowrap;

  gap: 10px;
}

.tags_list {
  /*outline: red 1px solid;*/
  display: flex;
  flex-wrap: nowrap;
}

.tags_list_poster {
  /*outline: red 1px solid;*/
  position: absolute;
  /*transform: translate(+7.5vw);*/

  display: flex;
  flex-wrap: nowrap;
  flex-direction: column;
  opacity: 1;
  visibility: visible;

  transition: 0.3s ease-in-out;

}

.open .tags_list_poster {
  opacity: 0;
  visibility: hidden;
}

.editor_button {
  position: absolute;
  transform: translate(174px, 2px);
}

.rank_content {
  /*outline: red 1px solid;*/

  display: flex;
  flex-wrap: nowrap;
  margin: 0;
}

.ranking_title {
  /*outline: red 1px solid;*/

  display: flex;
  flex-wrap: nowrap;
  margin: 0;
}
</style>