<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import BadgeTooltip from "@/components_V2/media_container/movie_container/badgeTooltip.vue";

let props = defineProps(["data", "min_size"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

const tag_container = ref()
const tooltip_container = ref()


function compute_tag_position() {
  let tag = tag_container.value
  let tip = tooltip_container.value.$refs['tooltip_container']

  let tag_box = tag.getBoundingClientRect()
  let tip_box = tip.getBoundingClientRect()


  if (tag_box.x < (window.innerWidth / 2)) {
    tip.style.transform = `translate(${-15}px,${-tag_box.height - tip_box.height - 20}px)`;
  } else {
    tip.style.transform = `translate(${-tip_box.width - 20}px,${-tag_box.height - tip_box.height - 20}px)`;
  }


}


onMounted(() => {
  compute_tag_position()
})
</script>

<template>
  <div class="tag_box">
    <img ref="tag_container" class="tag_image" v-lazy="`/tags/icons/${data['tier']}/${data['image_path']}`">
    <badge-tooltip :text_limit="10" :text_size="1" ref="tooltip_container" class="badge_tooltip" :data="data"></badge-tooltip>
  </div>
</template>

<style scoped>

.tag_box:hover .badge_tooltip {
  opacity: 100%;
  visibility: visible;
  transition: 50ms;

}

.tag_box {
  width: calc(v-bind(min_size) * 0.2px);
  height: calc(v-bind(min_size) * 0.2px);
}

.tag_image {
  width: 100%;
  height: 100%;
}
</style>