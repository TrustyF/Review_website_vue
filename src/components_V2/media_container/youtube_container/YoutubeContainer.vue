<script setup>
import {inject, onMounted, watch, ref, computed, provide} from "vue";
import BadgesHorizontal from "@/components_V2/media_container/youtube_container/badgesHorizontal.vue";

let props = defineProps(["data", "container_scale", "container_size"]);
let emits = defineEmits(["media_data"]);
const curr_api = inject("curr_api");

const poster_size = computed(() => [
  props['container_size'][0] * props['container_scale'],
  props['container_size'][1] * props['container_scale']
])

function convert_seconds_to_time(f_seconds) {
  let minutes = f_seconds % 60
  let hours = (f_seconds - minutes) / 60

  if (hours < 1) {
    return minutes + 'min'
  } else {
    return hours + 'h ' + minutes;
  }
}

</script>

<template>
  <div class="movie_container_wrapper" @click="emits('media_data',data)">

    <img class="poster" alt="poster" v-lazy="`${curr_api}/media/get_image?id=${data['id']}`"/>

    <badges-horizontal :data="data" :bounds="poster_size"></badges-horizontal>

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
    </div>

  </div>
</template>

<style scoped>
.movie_container_wrapper {
  /*outline: 1px solid red;*/
  position: relative;
  border-radius: 8px;
  width: v-bind(poster_size [0] + 'px');
  height: fit-content;

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
  padding: 12px;
  margin-top: calc(v-bind(poster_size [1]) * 0.01px);
}

.title {
  /*font-size: 1.1em;*/
  font-size: calc(v-bind(poster_size [1]) * 0.005em);
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
  font-size: calc(v-bind(poster_size [1]) * 0.004em);
  color: rgba(255, 255, 255, 0.5);
}
</style>