<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

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
        <h1 class="description_title">{{ data['name'] }}</h1>

        <div class="description_genres_list">
          <div class="genre_tag" v-for="genre in data['genres']" :key="genre['id']">{{ genre['name'] }}</div>
        </div>

      </div>

      <h2 class="description_subtitle">{{
          data['release_date'].substring(0, 4) + ' • ' +
          convert_seconds_to_time(data['runtime'])
        }}</h2>
      <p class="description">{{ data['overview'] }}</p>

    </div>

  </div>
</template>

<style scoped>

.header_wrapper {
  outline: 1px solid red;
  /*margin: 30px 30px 0 30px;*/
  display: flex;
  height: 50%;
}

.description_wrapper {
  outline: 2px solid orange;
  padding: 10px;
  display: flex;
  flex-flow: column;
  gap: 10px;
}
.description_title_wrapper {
  /*outline: 1px solid red;*/
  display: flex;
  flex-flow: column nowrap;
}


.description_title {
  font-weight: bold;
  font-size: 1.5em;
}

.description_subtitle {
  font-size: 0.9em;
  color: rgb(150, 150, 150);
}

.description {
  font-size: 0.8em;
  line-height: 1.2em;
}
.description_genres_list {
  /*outline: 2px solid green;*/
  margin-top: 5px;
  display: flex;
  flex-flow: row;
  gap: 5px;
}
.genre_tag {
  padding: 5px;
  /*background: white;*/
  /*color: black;*/
  border-radius: 5px;
  font-size: 0.8em;
  outline: 1px white solid;
}
</style>