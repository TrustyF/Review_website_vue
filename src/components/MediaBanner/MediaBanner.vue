<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MovieContainer from '@/components/media_container/movie_container/MovieContainer.vue'
import axios from "axios";

let props = defineProps({
  media_type: {
    type: String,
    default: null,
  },
  order: {
    type: String,
    default: null,
  },
  ratings: {
    type: Array,
    default: null,
  },
  tier_lists: {
    type: Array,
    default: null,
  },
});
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");
const session_seed = inject("session_seed");
const is_mobile = inject("is_mobile");

let media = ref(new Array(10).fill().map((e, i) => {
  return {
    name: '',
    release_date: '',
  }
}))

async function get_media() {

  const url = new URL(`${curr_api}/media/get`)
  const params = {
    'limit': 20,
    'page': 0,
    'type': props.media_type,
    'order': props.order,
    'ratings': props.ratings,
    'tier_lists': props.tier_lists,
    'session_seed': session_seed,
    'user_rating_sort_override': true,
  }

   let result = await axios(
      {
        method: 'POST',
        url: url,
        headers: {"Content-Type": "application/json"},
        data: JSON.stringify(params)
      })
      .catch(error => {
        console.log('media_banner_get_media', error.response)
        return []
      })

  console.log(result)
  if (result.status !== 200) return

  media.value = result.data
  // sort tags by color
  const priority = ['gold', 'green', 'purple', 'silver', 'red']
  media.value.forEach((entry, i) => {
    media.value[i].tags.sort((a, b) => {
      const fi = priority.indexOf(a.tier)
      const si = priority.indexOf(b.tier)
      return fi - si
    })
  })
}

onMounted(() => {
  get_media()
})

</script>

<template>
  <div class="banner_wrapper">
    <div class="banner_fade"></div>
    <div class="scroll_container">
      <div class="scroll_content" v-for="med in media" :key="med.id">
        <movie-container
            :data="med"
            :lazy_poster="false"
            :scale_mul="!is_mobile ? 0.3:0.2"
            :size_override="[500,750]"
        ></movie-container>
      </div>
    </div>
<!--    <div class="scroll_container" v-else>-->
<!--      <img class="spinner" alt="spinner" :src="spinner">-->
<!--    </div>-->

  </div>
</template>

<style scoped>
.banner_wrapper {
  /*outline: 1px solid red;*/
  /*border: 0.1em dotted #41404d;*/
  border-radius: 10px;
  /*padding: 15px 0 15px 15px;*/
  position: relative;
  display: flex;
  align-items: center;
}

.scroll_container {
  /*position: relative;*/
  overflow-x: scroll;
  /*overflow-y: hidden;*/
  display: flex;
  flex-flow: row;
  gap: 20px;
  padding-bottom: 20px;
  /*white-space:nowrap;*/
  /*outline: 1px solid red;*/
}
::-webkit-scrollbar {
  background-color: #f5f5f5;
  border-radius: 10px;
  width: 7px;
  height: 2px;
}
::-webkit-scrollbar-thumb {
  background-color: #000000;
  border-radius: 10px;
}

.spinner {
  position: relative;
  height: 50%;
  /*object-fit: cover;*/
  /*margin: 0 auto 0 auto;*/
}

.banner_fade {
  /*background-color: red;*/
  pointer-events: none;
  width: 100%;
  height: 100%;
  z-index: 5;
  position: absolute;
  background: linear-gradient(to right, rgba(19, 18, 21, 0) 90%, rgba(19, 18, 21, 1) 100%);
}

</style>