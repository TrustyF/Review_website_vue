<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import diff3 from '/ui/diff_3.png'

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
  <img :src="diff3" class="star">
</template>

<style scoped>
.star {
  /*height: 100%;*/
  object-fit: scale-down;
}
</style>