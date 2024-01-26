<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import TierBox from "./TierBox.vue";

let props = defineProps(["box_size", "box_scale", "data"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

let tier_box_height = computed(() => (props['box_size'][1] * props['box_scale']) + 'px')
let tier_box_width = computed(() => (props['box_size'][0] * props['box_scale']) + 'px')
let feed_width = computed(() => (props['box_size'][0] * props['box_scale'] + 25) * 2 + 'px')

</script>

<template>
  <div class="tier_feed_wrapper">
    <tier-box :box_size="box_size" :b_width="tier_box_width" :b_height="tier_box_height"
              :box_data="box" v-for="box in data"
              :key="box"></tier-box>

    <tier-box :box_size="box_size" :b_width="tier_box_width" :b_height="tier_box_height"
              :box_data="{'name': 'Youtube debug','image': undefined,'link':'/youtube/youtube_debug'  }"></tier-box>
  </div>
</template>

<style scoped>
.tier_feed_wrapper {
  /*outline: 1px solid greenyellow;*/

  width: v-bind(feed_width);

  display: flex;
  flex-flow: row wrap;

  align-items: center;
  justify-items: center;

  margin: 50px auto auto auto;
  gap: 50px;
}

@media only screen and (max-width: 724px) {
  .tier_feed_wrapper {
    flex-flow: column nowrap;
    grid-gap: 20px;
  }
}
</style>