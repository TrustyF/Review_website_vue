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

function parse_diff(index) {
  if (index === undefined) return 'Accessible'
  if (index === 1) return 'Accessible'
  if (index === 2) return 'Involved'
  if (index === 3) return 'Hard'
  return 'Accessible'
}


</script>

<template>
  <div class="gauge_wrapper" :title="`Difficulty : ${parse_diff(diff)}`" v-if="diff">
<!--    <div v-if="diff >= 3" class="bg_dot"></div>-->
<!--    <div v-if="diff >= 2" class="bg_dot"></div>-->
<!--    <div v-if="diff >= 2" class="bg_dot"></div>-->
        <div v-if="diff === 3" class="gauge_bar" style="background-color: #e64432"></div>
        <div v-if="diff === 2" class="gauge_bar" style="background-color: #f1c40f"></div>
<!--        <div v-if="diff >= 2" class="gauge_bar" style="background-color: #1abc60"></div>-->
  </div>
</template>

<style scoped>
.gauge_wrapper {
  /*outline: 1px solid red;*/
  padding: 10px;
  position: relative;
  display: flex;
  flex-flow: row;
  gap: 3px;
}
.gauge_wrapper:hover::before {
  content: attr(title);
  background-color: #25222a;
  color: #ffffff;
  padding: 10px;
  border-radius: 5px;
  position: absolute;
  font-size: 0.8em;
  white-space: nowrap;
  transform: translate(-50%,-150%);
  filter: drop-shadow(1px 1px 2px black);
  z-index: 100;
}
.bg_dot {
  width: 1px;
  height: 5px;
  background: white;
  /*border-radius: 50%;*/
  filter: opacity(50%);
}

.gauge_bar {
  /*position: absolute;*/
  height: 5px;
  width: 5px;
  border-radius: 50%;
  opacity: 0.7;
  /*background:linear-gradient(to bottom,#c0392b 0%, #f1c40f 50%, #1abc9c 100%);*/
}

.gauge_text {
  position: absolute;
  left: 50%;
  transform: translate(-50%);
  font-size: 0.6em;
}
@media only screen and (max-width: 500px) {
  .gauge_wrapper:hover::before {
    transform: translate(-100%,-150%);
  }
}

</style>