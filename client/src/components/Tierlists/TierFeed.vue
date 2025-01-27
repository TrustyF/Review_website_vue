<script setup>
import {inject} from "vue";
import TierBox from "./TierBox.vue";

let props = defineProps(["box_size", "box_scale", "row_num", "data"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");
const edit_mode = inject("edit_mode");

</script>

<template>
  <div class="tier_feed_wrapper">
    <tier-box :box_size="box_size"
              :box_data="box" v-for="box in data"
              :key="box"></tier-box>
  </div>
</template>

<style scoped>
.tier_feed_wrapper {
  display: grid;
  grid-template-columns: repeat(v-bind(row_num), 1fr);

  justify-items: center;
  align-items: flex-start;

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