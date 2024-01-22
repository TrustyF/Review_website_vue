<script setup>
import {inject, onMounted, watch, ref, provide, computed} from "vue";
import BadgeExpanded from "../media_container/movie_container/sub_components/badgeExpanded.vue";

// let props = defineProps(["position", "data"]);
// let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

const tooltip_container = ref()

const tooltip_pos = inject("tooltip_badge_pos");
const tooltip_data = inject("tooltip_badge_data");
const tooltip_hover = inject("tooltip_badge_hover");

async function position_tooltip() {
  // hack to give time to the element to update it's size
  await setTimeout(() => {
  }, 0.1)

  // position tooltip
  let style = tooltip_container.value.style
  let box = tooltip_container.value.getBoundingClientRect()

  let tooltip_x = tooltip_pos.value[0] - (box.width / 2)
  let tooltip_y = tooltip_pos.value[1] - 100

  style.top = `${tooltip_y}px`
  style.left = `${Math.max(0, tooltip_x)}px`
}

watch(tooltip_data, (newV, oldV) => {
  position_tooltip()
})
onMounted(() => {
  // const resizer = new ResizeObserver(position_tooltip)
  // resizer.observe(tooltip_container.value)
})
</script>

<template>
  <div ref="tooltip_container" :class="tooltip_hover ? 'tooltip_wrapper visible' : 'tooltip_wrapper'">
    <badge-expanded class="badge" :text_size="1" :data="tooltip_data"></badge-expanded>
  </div>
</template>

<style scoped>
.tooltip_wrapper {
  /*outline: 1px solid red;*/
  max-width: 300px;

  position: absolute;
  left: 0;
  top: 0;
  /*right: 0;*/
  z-index: 1000;
  margin: 0 10px 0 10px;

  opacity: 0;
  visibility: hidden;
  transition: opacity 200ms;

  pointer-events: none;
  user-select: none;
}

.visible {
  opacity: 100%;
  visibility: visible;
}

.badge {
  opacity: 100%;
  visibility: visible;
  box-shadow: 0 0 5px black, 0 0 35px black
}
</style>