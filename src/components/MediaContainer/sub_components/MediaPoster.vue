<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

</script>

<template>
  <img v-lazy="`https://image.tmdb.org/t/p/w500${data['poster_path']}`" class="poster" alt="poster" draggable="false">
</template>

<style scoped>

</style>