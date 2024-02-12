<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps({
  diff: {
    type: Number,
    default: null,
  },
});
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="gauge_wrapper" v-if="diff">
    <div v-if="diff >= 3" class="gauge_bar" style="background-color: #c0392b;border-radius: 10px 10px 0 0"></div>
    <div v-if="diff >= 2" class="gauge_bar" style="background-color: #f1c40f"></div>
    <div v-if="diff >= 1" class="gauge_bar" style="background-color: #1abc60;border-radius: 0 0 10px 10px"></div>
  </div>
</template>

<style scoped>
.gauge_wrapper {
  width: 10px;
  height: 30px;
  outline: 2px solid #25222a;
  background-color: #25222a;
  border-radius: 10px;
  /*gap: 2px;*/
  /*clip-path: inset(0% 0% 0% 0% round 6px);*/

  display: flex;
  flex-flow: column;
  justify-content: flex-end;
}
.gauge_bar {
  height: 33%;
  width: 100%;
  /*background:linear-gradient(to bottom,#c0392b 0%, #f1c40f 50%, #1abc9c 100%);*/
}

</style>