<script setup>
import {inject, onMounted, watch, ref, computed, provide} from "vue";
import Rating from "@/components_V2/media_container/movie_container/rating.vue";
import Badge from "@/components_V2/media_container/movie_container/badge.vue";

let props = defineProps(["data", "container_scale", "container_size"]);
let emits = defineEmits(["media_data"]);
const curr_api = inject("curr_api");

const poster_size = computed(() => [
  props['container_size'][0] * props['container_scale'],
  props['container_size'][1] * props['container_scale']
])
const min_size = computed(() => Math.min(poster_size.value[0], poster_size.value[1]))

function convert_seconds_to_time(f_seconds) {
  let minutes = f_seconds % 60
  let hours = (f_seconds - minutes) / 60

  if (hours < 1) return minutes + ' min'
  return hours + 'h ' + minutes;
}

</script>

<template>
  <div class="movie_container_wrapper" @click="emits('media_data',data)">

    <img class="poster" alt="poster" v-lazy="`${curr_api}/media/get_image?id=${data['id']}`"/>
    <div class="poster_gradient"></div>

    <Rating class="ratings" :data="data" :max_size="min_size"></Rating>

    <div class="footer_wrapper">

      <p class="title" :title="data['name']">{{ data['name'] }}</p>

      <div class="secondary_info">
        <h2 class="date">{{ data['release_date'].substring(0, 4) }}</h2>
        <h2 class="date" v-if="data['runtime']>0">•</h2>
        <h2 class="date" v-if="data['runtime']>0">{{ convert_seconds_to_time(data['runtime']) }}</h2>
        <h2 class="date" v-if="data['seasons']>0">•</h2>
        <h2 class="date" v-if="data['seasons']>0">{{ data['seasons'] + ' s' }} </h2>
        <h2 class="date" v-if="data['episodes']>0">{{ data['episodes'] + ' ep' }} </h2>
      </div>

      <div class="tags_wrapper" v-if="data['tags']!==undefined && data['tags']!==null">
        <div v-for="tag in data['tags']" :key="tag['id']">
          <badge :data="tag" :min_size="min_size" :show_title="true"></badge>
        </div>
      </div>

    </div>

  </div>
</template>

<style scoped>
.movie_container_wrapper {
  /*outline: 1px solid red;*/
  position: relative;
  display: flex;
  flex-flow: column nowrap;

  width: v-bind(poster_size [0] + 'px');
  min-height: v-bind(poster_size [1] + 'px');
  height: fit-content;

  background-color: #25222a;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.75);

  border-radius: 8px;
}

.poster {
  width: v-bind(poster_size [0] + 'px');
  height: v-bind(poster_size [1] + 'px');

  padding: 0;
  margin: 0;
  inset: 0;

  border-radius: 8px 8px 0 0;
  object-fit: cover;
}

.poster_gradient {
  content: "";
  position: absolute;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 90%, rgba(0, 0, 0, 0.5) 100%);
  left: 0;
  top: 0;
  width: v-bind(poster_size [0] + 'px');
  height: v-bind(poster_size [1] + 'px');
}

.ratings {
  position: absolute;
  margin-left: 5px;
  left: 0;
  top: 0;
  transform: translate(0, v-bind(poster_size [1] + 'px')) translate(0, -50%);
}

.footer_wrapper {
  padding: 12px;
  margin-top: calc(v-bind(min_size) * 0.05px);
}

.title {
  /*font-size: 1.1em;*/
  font-size: calc(v-bind(min_size) * 0.005em);
  line-height: normal;
  font-weight: 500;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

.secondary_info {
  display: flex;
  gap: 5px;
}

.date {
  /*margin-top: 5px;*/
  font-size: calc(v-bind(min_size) * 0.004em);
  color: rgba(255, 255, 255, 0.5);
}

.tags_wrapper {
  /*outline: 1px solid red;*/
  width: v-bind(poster_size [0] + 'px');
  position: absolute;

  left: 0;
  top: 0;

  display: flex;
  flex-flow: column wrap;
  gap: 5px;

  padding: 5px;
  transform: translate(-10px, 0);
  visibility: hidden;
  opacity: 0;
  z-index: 20;

  transition: 400ms;
  transition-delay: 700ms;
}

.movie_container_wrapper:hover .tags_wrapper {
  visibility: visible;
  opacity: 100%;
  transform: translate(0, 0);
  transition-delay: 0ms;
  transition: 50ms;
}

</style>