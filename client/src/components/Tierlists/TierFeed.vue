<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import TierBox from "./TierBox.vue";

let props = defineProps(["box_size","data"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="tier_feed_wrapper">
    <tier-box :box_size="box_size" :box_data="box" v-for="box in data" :key="box"></tier-box>
  </div>
</template>

<style scoped>
.tier_feed_wrapper {
  /*outline: 1px solid greenyellow;*/

  padding-top: 40px;
  display: flex;
  flex-flow: row wrap;

  justify-content: space-evenly;
  align-items: center;
  justify-items: center;

  grid-gap: 10px;
}
@media only screen and (max-width: 724px) {
  .tier_feed_wrapper{
    flex-flow: column nowrap;
    grid-gap: 20px;
  }
}
</style>