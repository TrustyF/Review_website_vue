<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaReview from "@/components/MediaContainer/Master/Base/sub_components/MediaReview.vue";
import ExpandedHeaderRating from "@/components/MediaContainer/Master/Expanded/sub_components/ExpandedHeaderRating.vue";

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

      <div class="description_title">{{ data['name'] }}</div>

      <div class="desc_subtitle_wrapper">
        <h2 class="desc_subtitle">{{ data['release_date'].substring(0, 4) }}</h2>

        <h2 class="desc_subtitle" v-if="data['runtime']>0">{{ ' • ' + convert_seconds_to_time(data['runtime']) }}</h2>
        <h2 class="desc_subtitle" v-if="data['seasons']>0">{{ ' • ' + data['seasons'] + ' seasons' }} </h2>
        <h2 class="desc_subtitle" v-if="data['episodes']>0">{{ ' • ' + data['episodes'] + ' episodes' }} </h2>
      </div>

      <div class="description_title_wrapper">
        <div class="description_genres_list">
          <div class="genre_tag" v-for="genre in data['genres']" :key="genre['id']">{{ genre['name'] }}</div>
        </div>
        <expanded-header-rating :data="data"></expanded-header-rating>
      </div>

      <p class="description">{{ data['overview'] }}</p>

    </div>

  </div>
</template>

<style scoped>

.header_wrapper {
  /*outline: 2px solid orange;*/
  display: flex;
}

.description_wrapper {
  /*outline: 2px solid orange;*/
  padding: 5px 0 0 20px;
  display: flex;
  flex-flow: column;
  gap: 10px;
}

.description_title_wrapper {
  /*outline: 1px solid red;*/
  display: flex;
  flex-flow: column nowrap;
  gap: 10px;
}


.description_title {
  /*outline: 1px solid orange;*/
  /*height: 21px;*/
  font-weight: bold;
  font-size: 1.5em;
  text-shadow: 1px 1px 3px black;
}

.desc_subtitle_wrapper {
  display: flex;
  gap: 3px;
}

.desc_subtitle {
  font-size: 0.9em;
  color: rgb(150, 150, 150);
}

.description {
  /*outline: 1px solid green;*/
  font-size: 0.8em;
  line-height: 1.3em;
  /*height: 300px;*/

  overflow: scroll;
}

.description_genres_list {
  /*outline: 1px solid green;*/
  /*margin-top: 5px;*/
  display: flex;
  flex-flow: row wrap;
  gap: 10px;
}

.genre_tag {
  padding: 5px;
  /*background: white;*/
  /*color: black;*/
  border-radius: 5px;
  font-size: 0.8em;
  outline: 1.5px grey solid;
  box-shadow: 2px 2px 5px #000000;
}

@media only screen and (max-width: 500px) {
  .description_wrapper {
    /*outline: 2px solid orange;*/
    padding: 10px;
    display: flex;
    flex-flow: column;
    gap: 10px;
  }
}
</style>