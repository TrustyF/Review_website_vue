<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import TierBox from "./TierBox.vue";
import dont_thug_img from "/tier_list_images/dont_thug_me.jpg"

let props = defineProps(["box_size", "box_scale", "row_num", "data"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");
const edit_mode = inject("edit_mode");

let tier_box_height = computed(() => (props['box_size'][1] * props['box_scale']) + 'px')
let tier_box_width = computed(() => (props['box_size'][0] * props['box_scale']) + 'px')
let feed_width = computed(() => (props['box_size'][0] * props['box_scale'] + 25) * props['row_num'] + 'px')

let debug = {
  'name': 'Youtube Debug',
  'image': dont_thug_img,
  'link': '/youtube/youtube_debug'
}

</script>

<template>
  <div class="tier_feed_wrapper">
    <tier-box :box_size="box_size" :b_width="tier_box_width" :b_height="tier_box_height"
              :box_data="box" v-for="box in data"
              :key="box"></tier-box>

    <tier-box v-if="edit_mode" :box_size="box_size" :b_width="tier_box_width" :b_height="tier_box_height"
              :box_data="debug"></tier-box>
  </div>

</template>

<style scoped>
.tier_feed_wrapper {
  /*outline: 1px solid greenyellow;*/

  width: v-bind(feed_width);

  /*display: flex;*/
  /*flex-flow: row wrap;*/
  display: grid;
  grid-template-columns: repeat(v-bind(row_num), 1fr);

  align-items: center;
  /*align-content: center;*/
  /*justify-content: center;*/
  justify-items: center;

  margin: 100px auto auto auto;
  padding-bottom: 30px;

  gap: 25px;
}

@media only screen and (max-width: 1000px) {
  .tier_feed_wrapper {
    width: 90%;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    margin: 100px auto auto auto;

    grid-gap: 30px;
  }
}
</style>