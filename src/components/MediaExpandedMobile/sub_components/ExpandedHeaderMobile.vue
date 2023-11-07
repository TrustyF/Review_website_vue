<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaReview from "@/components/MediaContainer/sub_components/MediaReview.vue";
import ExpandedHeaderRatingMobile from "@/components/MediaExpandedMobile/sub_components/ExpandedHeaderRatingMobile.vue";

let props = defineProps(["data"]);

function convert_seconds_to_time(f_seconds) {
  let minutes = f_seconds % 60
  let hours = (f_seconds - minutes) / 60
  return hours + 'h ' + minutes + 'm';
}
</script>

<template>
  <div class="header_wrapper">

    <div class="description_wrapper">

      <div class="description_title_wrapper">

        <div class="description_title">{{ data['name'] }}</div>

        <div class="description_genres_list">
          <div class="genre_tag" v-for="genre in data['genres'].slice(0,3)" :key="genre['id']">{{ genre['name'] }}</div>
        </div>

      </div>


      <div class="desc_subtitle_wrapper">
        <h2 class="desc_subtitle">{{ data['release_date'].substring(0, 4) }}</h2>

        <h2 class="desc_subtitle" v-if="data['runtime']>0">{{ ' • ' + convert_seconds_to_time(data['runtime']) }}</h2>
        <h2 class="desc_subtitle" v-if="data['seasons']>0">{{ ' • ' + data['seasons'] + ' seasons' }} </h2>
        <h2 class="desc_subtitle" v-if="data['episodes']>0">{{ ' • ' + data['episodes'] + ' episodes' }} </h2>
      </div>


<!--      <p class="description">{{ data['overview'] }}</p>-->

      <expanded-header-rating-mobile :data="data"></expanded-header-rating-mobile>

    </div>

  </div>
</template>

<style scoped>

.header_wrapper {
  /*outline: 2px solid orange;*/
  width: 100%;
  overflow: hidden;
  display: flex;
}

.description_wrapper {
  /*outline: 2px solid orange;*/
  padding: 5px 0 0 20px;
  display: flex;
  flex-flow: column;
  gap: 5px;
}

.description_title_wrapper {
  /*outline: 1px solid red;*/
  display: flex;
  flex-flow: column nowrap;
}


.description_title {
  /*outline: 1px solid orange;*/
  font-weight: bold;
  font-size: 1em;
  text-shadow: 1px 1px 3px black;
}

.desc_subtitle_wrapper {
  display: flex;
  gap: 2px;
}

.desc_subtitle {
  font-size: 0.7em;
  color: rgb(150, 150, 150);
}

.description {
  /*outline: 1px solid green;*/
  font-size: 0.8em;
  line-height: 1.2em;
  /*height: 300px;*/
  overflow: scroll;
}

.description_genres_list {
  /*outline: 1px solid green;*/
  width: 100%;
  margin-top: 5px;
  display: flex;
  flex-flow: row nowrap;
  gap: 10px;
}

.genre_tag {
  padding: 5px;
  max-width: 50px;
  overflow: hidden;
  text-overflow: ellipsis;
  /*background: white;*/
  /*color: black;*/
  white-space: nowrap;
  border-radius: 5px;
  font-size: 0.5em;
  outline: 1.5px grey solid;
  box-shadow: 2px 2px 5px #000000;
}
expanded-header-rating-mobile {
  bottom: 0;
}
</style>