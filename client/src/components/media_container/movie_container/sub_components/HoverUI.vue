<script setup>
import {inject, onMounted, watch, ref, computed, defineAsyncComponent} from "vue";
import {log_event} from "/src/scripts/log_events";

const badge = defineAsyncComponent(() => import("@/components/media_container/movie_container/sub_components/badge.vue"))

let props = defineProps({
  data: {
    type: Object,
    default: null,
  },
  poster_size: {
    type: Array,
    default: () => [0, 0],
  },
  min_size: {
    type: Number,
    default: null,
  },
});
let emits = defineEmits(["test"]);

let edit_mode = inject('edit_mode')
let edit_pane_open = inject('edit_pane_open')
let add_pane_open = inject('add_pane_open')
let selected_media = inject('selected_media')
let media_detail_pane_open = inject("media_detail_pane_open");

let dropped_badge = {
  image_path: "103201",
  name: "Dropped",
  overview: "Didn't care enough to finish it",
  tier: "red"
}

const curr_api = inject("curr_api");
let vis_container_content_rating = inject('vis_container_content_rating')

function emitted_media_to_edit_pane(e) {
  e.preventDefault()
  if (!edit_pane_open.value && !add_pane_open.value) {
    edit_pane_open.value = true
  }
  selected_media.value = props.data
}

function push_to_details() {
  selected_media.value = props['data']
  media_detail_pane_open.value = true
}

function open_link_new_tab(path) {
  window.open(path, '_blank');
  log_event('open_external', 'nav', props.data.name)
}

function sort_tags(arr) {
  // sort tags by color
  const priority = ['gold', 'green', 'purple', 'silver', 'red']
  arr.sort((a, b) => {
    const fi = priority.indexOf(a.tier)
    const si = priority.indexOf(b.tier)
    return fi - si
  })

  return arr
}

</script>

<template>
  <div class="poster_gradient"></div>

  <div class="content_rating" v-if="vis_container_content_rating && data['content_rating']!==undefined">
    <h1 style="font-size: 0.8em;margin-top: 2px">+</h1>
    <h2 style="color: white">{{ data['content_rating']['age'] }}</h2>
  </div>

  <div class="tags_wrapper" v-if="(data['tags']!==undefined && data['tags']!==null && data['tags'].length > 0) || data['is_dropped']">

    <div v-for="tag in sort_tags(data['tags'])" :key="tag['id']" class="tag_vis_container">
      <badge :data="tag" :min_size="min_size" :show_title="false"></badge>
    </div>

    <div style="pointer-events: auto;width: fit-content" v-if="data['is_dropped']">
      <badge :data="dropped_badge" :min_size="min_size" :show_title="false"></badge>
    </div>
  </div>

  <div class="edit_tools_wrapper">
    <div v-if="edit_mode" class="edit_tool bi-pencil-fill" @click.stop="emitted_media_to_edit_pane"/>
    <div v-if="data['video_link']" class="edit_tool bi-play-fill" title="go to video"
         @click.stop="open_link_new_tab(data['video_link'])"/>
    <div v-if="data['external_link']" class="edit_tool bi-box-arrow-up-right" title="go to external website"
         @click.stop="open_link_new_tab(data['external_link'])"/>
  </div>

</template>

<style scoped>

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


.content_rating {
  pointer-events: none;

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

.edit_tools_wrapper {
  pointer-events: none;

  z-index: 100;
  /*width: v-bind(poster_size [0] + 'px');*/
  position: absolute;

  display: flex;
  flex-flow: column;
  /*gap: 5px;*/

  align-items: center;

  right: 0;
  top: 0;

  transform: translate(10px, 0);
  visibility: hidden;
  opacity: 0;
  transition: 400ms;
  transition-delay: 700ms;
}

.edit_tool {
  /*outline: 1px solid red;*/
  border: unset;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px;
  pointer-events: auto;
  cursor: pointer;
  font-size: 0.8em;

  width: calc(v-bind(min_size) * 0.15px);
  height: calc(v-bind(min_size) * 0.15px);

  filter: drop-shadow(0.05em 0 0.01em black) drop-shadow(0 0.05em 0.01em black) drop-shadow(-0.05em 0 0.01em black) drop-shadow(0 -0.05em 0.01em black) drop-shadow(1px 1px 3px black);
  border-radius: 5px;
}

.tags_wrapper {
  position: absolute;

  left: 0;
  top: 0;

  display: flex;
  flex-flow: column wrap;
  gap: 5px;
  padding: 5px;
  z-index: 20;

  pointer-events: auto;
  width: fit-content;

  transform: translate(-10px, 0);
  visibility: hidden;
  opacity: 0;

  transition: 400ms;
  transition-delay: 700ms;
}


.movie_container_wrapper:hover .tags_wrapper,
.movie_container_wrapper:hover .edit_tools_wrapper {
  visibility: visible;
  opacity: 100%;
  transform: translate(0, 0);
  transition-delay: 0ms;
  transition: 50ms;
}

</style>