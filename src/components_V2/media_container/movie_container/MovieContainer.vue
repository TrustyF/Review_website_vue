<script setup>
import {inject, onMounted, watch, ref, computed, provide} from "vue";
import Badges from "@/components_V2/media_container/movie_container/badges.vue";

let props = defineProps(["data", "container_scale", "container_size"]);
let emits = defineEmits(["media_data"]);
const curr_api = inject("curr_api");

const poster_size = computed(() => [
  props['container_size'][0] * props['container_scale'],
  props['container_size'][1] * props['container_scale']
])

</script>

<template>
  <div class="movie_container_wrapper" @click="emits('media_data',data)">

    <img class="poster" alt="poster" v-lazy="`${curr_api}/media/get_image?id=${data['id']}`"/>

    <badges :data="data" :bounds="poster_size"></badges>

    <div class="footer_wrapper">
      <p class="title">{{ data['name'] }}</p>
      <p class="date">{{ new Date(data['release_date']).getFullYear() }}</p>
    </div>

  </div>
</template>

<style scoped>
.movie_container_wrapper {
  /*outline: 1px solid red;*/
  position: relative;
  border-radius: 8px;
  width: v-bind(poster_size [0] + 'px');

  background-color: #25222a;
}

.poster {
  width: v-bind(poster_size [0] + 'px');
  height: v-bind(poster_size [1] + 'px');
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);

  border-radius: 8px 8px 0 0;
  object-fit: cover;
}

.footer_wrapper {
  padding: 7px;
  margin-top: 15px;
}

.title {
  /*font-size: 1.1em;*/
  font-size: calc(v-bind(poster_size[0]) * 0.006em);
  /*line-height: normal;*/
  font-weight: 500;
}

.date {
  margin-top: 5px;
  font-size: calc(v-bind(poster_size[0]) * 0.004em);
  color: rgba(255, 255, 255, 0.5);
}
</style>