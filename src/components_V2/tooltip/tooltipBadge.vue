<script setup>
import {inject, onMounted, watch, ref, provide, computed} from "vue";
import BadgeExpanded from "../media_container/movie_container/badgeExpanded.vue";

// let props = defineProps(["position", "data"]);
// let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

const tooltip_pos = inject("tooltip_badge_pos");
const tooltip_data = inject("tooltip_badge_data");
const tooltip_hover = inject("tooltip_badge_hover");

</script>

<template>
  <div :class="tooltip_hover ? 'tooltip_wrapper visible' : 'tooltip_wrapper'">
    <badge-expanded class="badge" :text_size="1" :data="tooltip_data"></badge-expanded>
  </div>
</template>

<style scoped>
.tooltip_wrapper {
  max-width: 300px;
  transform: translate(v-bind(tooltip_pos [0] + 'px'),v-bind(tooltip_pos [1] + 'px')) translate(-50%,-150%);

  position: absolute;
  left: 0;
  top  : 0;
  z-index: 1000;

  opacity: 0;
  visibility: hidden;
  /*transition: 50ms opacity;*/

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