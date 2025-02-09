<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["data", "min_size","show_title"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

const tooltip_pos = inject("tooltip_badge_pos");
const tooltip_data = inject("tooltip_badge_data");
const tooltip_hover = inject("tooltip_badge_hover");

const tag_container = ref(null)

function emit_tooltip_data() {
  if (tag_container.value === null) return
  let tag_box = tag_container.value.getBoundingClientRect()
  let tag_position = [tag_box.x + (tag_box.width / 2), tag_box.y + (tag_box.height / 2) + document.documentElement.scrollTop]

  tooltip_hover.value = true
  tooltip_pos.value = tag_position
  tooltip_data.value = props['data']

  // console.log(tooltip_pos.value[0], tooltip_pos.value[1])
}

function close_tooltip() {
  tooltip_hover.value = false
}

</script>

<template>
  <div class="tag_box" @mouseover="emit_tooltip_data" @mouseleave="close_tooltip">
    <img v-if="data['tier'] && data['image_path']" ref="tag_container" lazy="loading" class="tag_image"
         v-lazy="`${curr_api}/static/tags/icons/${data['tier']}/${data['image_path']}.webp`">
    <h1 v-if="show_title" class="tag_title">{{ data['name'] }}</h1>
  </div>
</template>

<style scoped>

.tag_box {
  /*width: calc(v-bind(min_size) * 0.2px);*/
  height: calc(v-bind(min_size) * 0.2px);

  display: flex;
  align-items: center;
  width: fit-content;
  /*gap: calc(v-bind(min_size) * 0.05px);*/

  box-shadow: 0 0 calc(v-bind(min_size) * 0.02px) #131215;
  border-radius: calc(v-bind(min_size) * 50px);
  background-color: #2b2a34;

  overflow: hidden;

  -webkit-animation: fadein 0.5s; /* Safari, Chrome and Opera > 12.1 */
  -moz-animation: fadein 0.5s; /* Firefox < 16 */
  -ms-animation: fadein 0.5s; /* Internet Explorer */
  -o-animation: fadein 0.5s; /* Opera < 12.1 */
  animation: fadein 0.5s;
}

.tag_image {
  /*width: 100%;*/
  height: 100%;
  filter: drop-shadow(0 0 3px black);
  opacity: 1;
  transition: opacity 0.5s;
}
.tag_image[lazy=loading] {
  opacity: 0;
}
.tag_title {
  font-size: calc(v-bind(min_size) * 0.004em);
  margin: calc(v-bind(min_size) * 0.05px);
  user-select: none;
}
.tag_title:after {
  /*outline: 1px solid red;*/
  content: "";
  margin: calc(v-bind(min_size) * 0.01px);
}
</style>