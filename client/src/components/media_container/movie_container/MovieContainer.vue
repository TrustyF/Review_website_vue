<script setup>
import {inject, onMounted, watch, ref, computed, provide} from "vue";
import Rating from "@/components/media_container/movie_container/sub_components/rating.vue";
import Badge from "@/components/media_container/movie_container/sub_components/badge.vue";
import {useRouter} from 'vue-router'
import not_found from '@/assets/ui/not_found.jpg'

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
});
let emits = defineEmits(["media_data"]);

let edit_mode = inject('edit_mode')
let media_scales = inject('media_scales')
let selected_media = inject('selected_media')
let edit_pane_open = inject('edit_pane_open')
let vis_container_content_rating = inject('vis_container_content_rating')


const curr_api = inject("curr_api");
const router = useRouter()

const media_type = computed(() => props['data']['media_type'] || 'movie')

const image_path = computed(() => format_image_path(props['data']['poster_path'], props['data']['external_id']))
const poster_size = computed(() => {
  if (props.size_override) {
    return [
      props.size_override[0] * props['scale_mul'],
      props.size_override[1] * props['scale_mul']
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
    return not_found
  }
}

function open_link_new_tab(path) {
  window.open(path, '_blank');
}

function emitted_media_to_edit_pane() {
  selected_media.value = props.data
  edit_pane_open.value = true
}

// onMounted(()=>{
//   console.log('media scales',media_scales.value)
//   console.log('media type',media_type.value)
// })

</script>

<template>
  <div class="movie_container_wrapper">

    <!--    todo compress dropped, add media type ?-->
    <!--    todo move tag images to backend -->
    <!--    todo remove short films from movies category -->
    <!--    todo remove youtube from home banners -->

    <!--    <div v-if="edit_mode"-->
    <!--         style="position:absolute;background-color: #25222a;left: 5px;top:5px;padding: 5px;font-size: 0.5em">-->
    <!--      &lt;!&ndash;      <p v-if="data['external_name']">external_name = {{ data['external_name'] }}</p>&ndash;&gt;-->
    <!--      <p v-if="data['content_rating']">content= {{ data['content_rating']['name'] }}</p>-->
    <!--      &lt;!&ndash;      <p v-if="data['genres']">genres= {{ data['genres'].map((elem)=>elem['name']) }}</p>&ndash;&gt;-->
    <!--      <p v-if="data['tier_lists']">tier_lists= {{ data['tier_lists'].map((elem) => elem['name']) }}</p>-->
    <!--      &lt;!&ndash;      <p v-if="data['themes']">themes= {{ data['themes'].map((elem)=>elem['name']) }}</p>&ndash;&gt;-->
    <!--      <p v-if="data['tags']">tags= {{ data['tags'].map((elem) => elem['name']) }}</p>-->
    <!--      &lt;!&ndash;      <p v-if="data['author']">author= {{ data['author'] }}</p>&ndash;&gt;-->
    <!--      &lt;!&ndash;      <p v-if="data['studio']">studio= {{ data['studio'] }}</p>&ndash;&gt;-->
    <!--      &lt;!&ndash;      <p v-if="data['release_date']">release_date= {{ data['release_date'] }}</p>&ndash;&gt;-->
    <!--            <p v-if="data['created_at']">created_at= {{ data['created_at'] }}</p>-->
    <!--      &lt;!&ndash;      <p>{{ image_path }}</p>&ndash;&gt;-->
    <!--    </div>-->

    <img v-if="lazy_poster" @click="open_link_new_tab(data['external_link'])" class="poster"
         v-lazy="image_path"/>
    <img v-else @click="open_link_new_tab(data['external_link'])" class="poster"
         :src="image_path"/>

    <div class="poster_gradient"></div>

    <div class="content_rating" v-if="vis_container_content_rating && data['content_rating']!==undefined">
      <h1 style="font-size: 0.8em;margin-top: 2px">+</h1>
      <h2 style="color: white">{{ data['content_rating']['age'] }}</h2>
    </div>

    <div v-if="data['is_dropped']" class="dropped_banner_wrapper">
      <div class="dropped_banner">Dropped</div>
    </div>

    <Rating v-if="data!==undefined" class="ratings" :data="data" :max_size="min_size"></Rating>

    <div class="footer_wrapper" @click="emitted_media_to_edit_pane">

      <p v-if="data['name']!==undefined" class="title" :title="data['name']">{{ data['name'] }}</p>

      <div class="secondary_info">
        <h2 class="date" v-if="data['release_date']!==undefined"> {{
            get_year_from_release_date(data['release_date'])
          }}</h2>
        <h2 class="date" v-if="data['runtime']>0">•</h2>
        <h2 class="date" v-if="data['runtime']>0">{{ convert_seconds_to_time(data['runtime']) }}</h2>
        <h2 class="date" v-if="data['seasons']>0">•</h2>
        <h2 class="date" v-if="data['seasons']>0">{{ data['seasons'] + ' s' }} </h2>
        <h2 class="date" v-if="data['episodes']>0">{{ data['episodes'] + ' ep' }} </h2>
<!--        <h2 class="date" v-if="data['content_rating'] && data['content_rating'].name">•</h2>-->
<!--        <h2 class="date" v-if="data['content_rating'] && data['content_rating'].name">-->
<!--          {{ data['content_rating'].name }}</h2>-->
      </div>

      <div class="tags_wrapper" v-if="data['tags']!==undefined && data['tags']!==null">
        <div v-for="tag in data['tags']" :key="tag['id']">
          <badge :data="tag" :min_size="min_size" :show_title="false"></badge>
        </div>
      </div>

    </div>

  </div>
<!--  <div style="background-color: red;width: 5000px;height:5000px;z-index:-1;position: fixed;left: 0;top: 0"></div>-->
</template>

<style scoped>
.movie_container_wrapper {
  /*outline: 1px solid red;*/
  cursor: pointer;
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
  pointer-events: none;
  content: "";
  position: absolute;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 90%, rgba(0, 0, 0, 0.5) 101%);
  left: 0;
  top: 0;
  width: v-bind(poster_size [0] + 'px');
  height: v-bind(poster_size [1] + 'px');
}

.dropped_banner_wrapper {
  position: absolute;
  left: 0;
  top: 0;
  width: v-bind(poster_size [0] + 'px');
  height: v-bind(poster_size [1] + 'px');
  clip-path: inset(0% 0% 0% 0% round 5%);
}

.dropped_banner {
  height: 30px;
  background-color: #c41717;
  transform: translate(v-bind(poster_size [0]/2 + 'px'), 0) rotate(45deg) translate(-10px, 30px);
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 0.8em;
  text-shadow: 1px 1px 1px black, 1px 1px 3px black;
  filter: drop-shadow(1px 1px 3px black);
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
  display: flex;
  gap: 5px;
}

.date {
  /*margin-top: 5px;*/
  font-size: calc(v-bind(min_size) * 0.004em);
  color: rgba(255, 255, 255, 0.5);
}
.content_rating {

  position: absolute;
  right: 0;
  top: 0;
  margin: 5px;

  font-size: calc(v-bind(min_size) * 0.005em);
  height: calc(v-bind(min_size) * 0.01em);
  width: calc(v-bind(min_size) * 0.01em);

  padding: calc(v-bind(min_size) * 0.001em);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;

  outline: 0.1em grey solid;

  color: lightgrey;
  background-color: black;
  filter: drop-shadow(1px 1px 2px black) drop-shadow(0px 0px 4px black);
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