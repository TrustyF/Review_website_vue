<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import CollapsedHeaderRating
  from "@/components/MediaContainer/Master/Collapsed/sub_components/CollapsedHeaderRating.vue";

let props = defineProps(["data"]);

function convert_seconds_to_time(f_seconds) {
  let minutes = f_seconds % 60
  let hours = (f_seconds - minutes) / 60
  return hours + 'h ' + minutes + 'm';
}
</script>

<template>

  <div class="description_wrapper">

    <div class="header">
      <div class="description_title">{{ data['name'] }}</div>

      <div class="desc_subtitle_wrapper">
        <h2 class="desc_subtitle">{{ data['release_date'].substring(0, 4) }}</h2>
        <h2 class="desc_subtitle" v-if="data['runtime']>0">{{ ' • ' + convert_seconds_to_time(data['runtime']) }}</h2>
        <h2 class="desc_subtitle" v-if="data['seasons']>0">{{ ' • ' + data['seasons'] + ' seasons' }} </h2>
        <h2 class="desc_subtitle" v-if="data['episodes']>0">{{ ' • ' + data['episodes'] + ' episodes' }} </h2>
      </div>
    </div>


    <div class="description_title_wrapper">
      <div class="description_genres_list">
        <div class="genre_tag" v-for="genre in data['genres']" :key="genre['id']">{{ genre['name'] }}</div>
      </div>
    </div>

    <div class="collapsed_rating_wrapper">
      <collapsed-header-rating :data="data"></collapsed-header-rating>
    </div>


<!--    <p class="description">{{ data['overview'].split(' ').slice(0,20).join(' ') + ' ...' }}</p>-->

  </div>

</template>

<style scoped>

.description_wrapper {
  /*outline: 1px solid orange;*/
  position: relative;
  padding: 5px 5px 5px 15px;
  display: flex;
  flex-flow: column;
  gap: 7px;

  justify-content: center;
}
.header {
  display: flex;
  flex-flow: column;
  gap: 2px;
}

.description_title_wrapper {
  /*outline: 1px solid red;*/
  display: flex;
  flex-flow: column nowrap;
  /*gap: 10px;*/
}

.collapsed_rating_wrapper {
  position: relative;
  width: 100%;
  /*margin-top: auto;*/
}

.description_title {
  /*outline: 1px solid orange;*/
  /*height: 21px;*/
  font-weight: 600;
  font-size: 1em;
  text-shadow: 1px 1px 3px black;
}

.desc_subtitle_wrapper {
  display: flex;
  gap: 3px;
}

.desc_subtitle {
  font-size: 0.5em;
  color: rgb(150, 150, 150);
}

.description {
  /*outline: 1px solid green;*/
  font-size: 0.6em;
  font-weight: 300;
  line-height: 1.3em;
  /*margin-bottom: 13px;*/
  /*max-height: 3em;*/

  overflow: scroll;
}

.description_genres_list {
  /*outline: 1px solid green;*/
  /*margin-top: 5px;*/
  display: flex;
  flex-flow: row wrap;
  gap: 5px;
}

.genre_tag {
  padding: 4px;
  /*background: white;*/
  /*color: black;*/
  border-radius: 5px;
  font-size: 0.5em;
  outline: 1.5px grey solid;
}


</style>