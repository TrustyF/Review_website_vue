<script setup>
import { inject, onMounted, watch, ref, computed } from "vue";

let props = defineProps({
    title : {
        type:String,
        default:null,
    },
  desc: {
    type: String,
    default: null,
  },
});
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="text_block">
    <h1>{{ title }}</h1>
    <p>{{ desc }}</p>
  </div>
</template>

<style scoped>
.text_block {
  margin-top: 100px;
  margin-bottom: -40px;

  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
  font-size: 1em;
  /*line-height: 1.5;*/
  word-wrap: break-word;
  font-weight: 400;
  text-align: center;
}
h1 {
  font-size: 3em;
  font-weight: 700;
  margin-bottom: 15px;
  /*text-decoration: 0.025em #575757 underline;*/
  /*text-underline-offset: 4px;*/
}
p {
  font-size: 1em;
  color: #b0b0b0;
}
</style>