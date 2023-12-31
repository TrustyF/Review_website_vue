<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import BadgeTooltip from "@/components_V2/media_container/movie_container/badgeExpanded.vue";

let props = defineProps(["data", "min_size"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

const tooltip_pos = inject("tooltip_badge_pos");
const tooltip_data = inject("tooltip_badge_data");
const tooltip_hover = inject("tooltip_badge_hover");

const tag_container = ref()

function emit_tooltip_data() {

  let tag_box = tag_container.value.getBoundingClientRect()
  let tag_position = [tag_box.x + (tag_box.width/2), tag_box.y + (tag_box.height/2) + document.documentElement.scrollTop]

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
    <img ref="tag_container" class="tag_image" v-lazy="`/tags/icons/${data['tier']}/${data['image_path']}`">
  </div>
</template>

<style scoped>

.tag_box {
  width: calc(v-bind(min_size) * 0.2px);
  height: calc(v-bind(min_size) * 0.2px);
}

.tag_image {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 3px black);
}
</style>