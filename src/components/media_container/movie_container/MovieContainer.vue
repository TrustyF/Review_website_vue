<script setup>
import {inject, onMounted, watch, ref, computed, provide, defineAsyncComponent} from "vue";
import {useRouter} from 'vue-router'
import {log_event} from "/src/scripts/log_events";
import {axios} from '@bundled-es-modules/axios';

const HoverUI = defineAsyncComponent(()=> import("@/components/media_container/movie_container/sub_components/HoverUI.vue"))
const DifficultyGauge = defineAsyncComponent(() => import("@/components/media_container/movie_container/sub_components/DifficultyGauge.vue"));
const Rating = defineAsyncComponent(() => import('@/components/media_container/movie_container/sub_components/rating.vue'));

let props = defineProps({
  data: {
    default: {
      name: 'Title',
      release_date: '2000',
      media_type: 'movie',
      user_rating: 9,
      public_rating: 9,
      scaled_public_rating: 9,
      poster_path: 'null',
    }
  },
  lazy_poster: {
    type: Boolean,
    default: true
  },
  scale_mul: {
    type: Number,
    default: 1
  },
  size_override: {
    type: Array,
    default: null
  },
  media_container_type_override: {
    type: String,
    default: null
  },
});
let emits = defineEmits(["media_data", "is_full_loaded"]);

let edit_mode = inject('edit_mode')
let media_scales = inject('media_scales')
let selected_media = inject('selected_media')

const curr_api = inject("curr_api");
const media_detail_pane_open = inject("media_detail_pane_open");
const router = useRouter()

const media_type = computed(() => props['data']['media_type'] || 'movie')

const image_path = computed(() => format_image_path(props['data']['poster_path'], props['data']['id']))
const poster_size = computed(() => {
  if (props.size_override) {
    return [
      props.size_override[0] * props['scale_mul'],
      props.size_override[1] * props['scale_mul']
    ]
  } else if (props.media_container_type_override) {
    return [
      (media_scales.value[props.media_container_type_override]['size'][0] *
          media_scales.value[props.media_container_type_override]['scale']) * props['scale_mul'],
      (media_scales.value[props.media_container_type_override]['size'][1] *
          media_scales.value[props.media_container_type_override]['scale']) * props['scale_mul'],
    ]
  } else {
    return [
      (media_scales.value[media_type.value]['size'][0] *
          media_scales.value[media_type.value]['scale']) * props['scale_mul'],
      (media_scales.value[media_type.value]['size'][1] *
          media_scales.value[media_type.value]['scale']) * props['scale_mul'],
    ]
  }

})
const min_size = computed(() => Math.min(poster_size.value[0], poster_size.value[1]))

function convert_seconds_to_time(f_seconds) {
  let minutes = f_seconds % 60
  let hours = (f_seconds - minutes) / 60

  if (hours < 1) return minutes + ' min'
  return hours + 'h ' + minutes;
}

function get_year_from_release_date(string) {

  if (typeof string === 'string') {
    return string.substring(0, 4)
  } else {
    return undefined
  }
}

function format_image_path(f_path, f_id) {
  if (f_path !== 'null' && f_path !== undefined) {
    return `${curr_api}/media/get_image?path=${f_path}&type=${props['data']['media_type']}&id=${f_id}`
  } else {
    return undefined
  }
}

async function download_poster(image_path){

  return await axios.get(image_path)
    .then(response => response.data)
}

function push_to_details() {
  selected_media.value = props['data']
  media_detail_pane_open.value = true
  log_event('open_movie', 'int', selected_media.value.name)
}

function emit_finished_loading() {
  emits("is_full_loaded", true)
  // poster_loaded.value = true
}

</script>
<template>
  <div class="movie_container_wrapper">

    <img datatype="img" @click="push_to_details" @loadeddata="emit_finished_loading" v-if="lazy_poster && image_path" class="poster"
         alt="" v-lazy="image_path" lazy="loading" draggable="false"/>
    <div v-else class="poster"></div>

    <difficulty-gauge :diff="data['difficulty']"></difficulty-gauge>

    <HoverUI :data="data" :poster_size="poster_size" :min_size="min_size"></HoverUI>

    <Rating v-if="data!==undefined" class="ratings" :data="data" :max_size="min_size"></Rating>

    <div class="footer_wrapper">

      <p v-if="data['name']!==undefined" class="title" :title="data['name']">{{ data['name'] }}</p>

      <div class="secondary_info">
        <h2 class="date" v-if="data['release_date']!==undefined"> {{
            get_year_from_release_date(data['release_date'])
          }}</h2>
        <h2 class="date" v-if="data['runtime']>0">•</h2>
        <h2 class="date" v-if="data['runtime']>0">{{ convert_seconds_to_time(data['runtime']) }}</h2>
        <h2 class="date" v-if="data['seasons']>0">•</h2>
        <h2 class="date" v-if="data['seasons']>0">{{ data['seasons'] + " " + 's' }} </h2>
        <h2 class="date" v-if="data['episodes']>0 && data['episodes']>0">
          {{ Math.round(data['episodes'] / data['seasons']) + ' ep' }} </h2>
        <!--        <h2 class="date" v-if="data['content_rating'] && data['content_rating'].name">•</h2>-->
        <!--        <h2 class="date" v-if="data['content_rating'] && data['content_rating'].name">-->
        <!--          {{ data['content_rating'].name }}</h2>-->
      </div>
    </div>
  </div>
</template>

<style scoped>
.movie_container_wrapper {
  /*cursor: pointer;*/
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

  -webkit-animation: fadein 0.25s; /* Safari, Chrome and Opera > 12.1 */
  -moz-animation: fadein 0.25s; /* Firefox < 16 */
  -ms-animation: fadein 0.25s; /* Internet Explorer */
  -o-animation: fadein 0.25s; /* Opera < 12.1 */
  animation: fadein 0.25s;
}

.poster {
  width: v-bind(poster_size [0] + 'px');
  height: v-bind(poster_size [1] + 'px');
  /*outline: 1px solid red;*/

  cursor: pointer;
  user-select: none;

  padding: 0;
  margin: 0;
  inset: 0;

  border-radius: 8px 8px 0 0;
  object-fit: cover;

  opacity: 1;
  transition: opacity 0.5s;
}

.poster[lazy=loading] {
  opacity: 0;
}

.ratings {
  position: absolute;
  margin-left: 5px;
  left: 0;
  top: 0;
  transform: translate(0, v-bind(poster_size [1] + 'px')) translate(0, -50%);
}

.footer_wrapper {
  min-height: calc(v-bind(min_size) * 0.18px);
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
  user-select: none;
  display: flex;
  gap: 5px;
}

.date {
  /*margin-top: 5px;*/
  font-size: calc(v-bind(min_size) * 0.004em);
  color: rgba(255, 255, 255, 0.5);
}
</style>