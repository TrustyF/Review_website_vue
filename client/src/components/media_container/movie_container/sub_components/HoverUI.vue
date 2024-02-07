<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import Badge from "@/components/media_container/movie_container/sub_components/badge.vue";
import crayon_img from '/ui/crayon.png'
import external_img from '/ui/external_link.png'

let props = defineProps({
  data: {
    type: Object,
    default: null,
  },
  poster_size: {
    type: Array,
    default: null,
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

const curr_api = inject("curr_api");
let vis_container_content_rating = inject('vis_container_content_rating')

function emitted_media_to_edit_pane() {
  if (!edit_pane_open.value && !add_pane_open.value) {
    edit_pane_open.value = true
  }
  selected_media.value = props.data
}

function open_link_new_tab(path) {
  window.open(path, '_blank');
}

</script>

<template>
  <div class="poster_gradient"></div>

<!--  <div class="blackout_hover"></div>-->

  <div class="content_rating" v-if="vis_container_content_rating && data['content_rating']!==undefined">
    <h1 style="font-size: 0.8em;margin-top: 2px">+</h1>
    <h2 style="color: white">{{ data['content_rating']['age'] }}</h2>
  </div>

  <div v-if="data['is_dropped']" class="dropped_banner_wrapper">
    <div class="dropped_banner">Dropped</div>
  </div>

  <div class="tags_wrapper" v-if="data['tags']!==undefined && data['tags']!==null">
    <div v-for="tag in data['tags']" :key="tag['id']">
      <badge :data="tag" :min_size="min_size" :show_title="false"></badge>
    </div>
  </div>

  <div class="edit_tools_wrapper">
    <img v-if="edit_mode" class="edit_tool" :src="crayon_img" @click="emitted_media_to_edit_pane">
    <img class="edit_tool" title="go to external website" :src="external_img"
         @click="open_link_new_tab(data['external_link'])">
  </div>

<!--  <input class="seen_checkbox" type="checkbox" title="mark as seen">-->


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

.blackout_hover {
  pointer-events: none;
  content: "";
  position: absolute;
  background: rgba(0,0,0,0.2);
  left: 0;
  top: 0;
  width: v-bind(poster_size [0] + 'px');
  height: v-bind(poster_size [1] + 'px');

  visibility: hidden;
  opacity: 0;
  transition: 400ms;
  transition-delay: 700ms;
}

.dropped_banner_wrapper {
  pointer-events: none;
  position: absolute;
  left: 0;
  top: 0;
  width: v-bind(poster_size [0] + 'px');
  height: v-bind(poster_size [1] + 'px');
  clip-path: inset(0% 0% 0% 0% round 5%);
}

.dropped_banner {
  pointer-events: none;
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

.seen_checkbox {
  cursor: pointer;
  position: absolute;
  right: 0;
  bottom: 0;
  margin: 5px;
  width: calc(v-bind(min_size) * 0.15px);
  height: calc(v-bind(min_size) * 0.15px);
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
  border: unset;
  padding: 5px;
  pointer-events: auto;
  cursor: pointer;

  width: calc(v-bind(min_size) * 0.15px);
  height: calc(v-bind(min_size) * 0.15px);

  /*background-color: #d8dbd3;*/
  /*box-shadow: 1px 1px 1px white, inset 1px 1px 0 #bdc0bb;*/

  filter: invert() drop-shadow(1px 1px 1px black) drop-shadow(0 0 3px black);
  border-radius: 5px;
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

.movie_container_wrapper:hover .edit_tools_wrapper,
.movie_container_wrapper:hover .tags_wrapper,
.movie_container_wrapper:hover .blackout_hover{
  visibility: visible;
  opacity: 100%;
  transform: translate(0, 0);
  transition-delay: 0ms;
  transition: 50ms;
}
</style>