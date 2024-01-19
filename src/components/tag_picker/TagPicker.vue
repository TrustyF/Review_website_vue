<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["test"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div></div>
</template>

<style scoped>

</style>