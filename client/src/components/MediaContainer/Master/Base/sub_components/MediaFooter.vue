<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="footer_wrapper">
    <h1>{{ data['name'] }}</h1>
    <h2>{{ new Date(data['release_date']).getFullYear() }}</h2>
  </div>
</template>

<style scoped>
.footer_wrapper {
  /*outline: 1px solid rebeccapurple;*/
  padding: 7px;
  margin-top: 13px;
}

h1 {
  font-size: 0.9em;
  font-weight: bold;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

h2 {
  margin-top: 3px;
  font-size: 0.7em;
  color: rgba(255, 255, 255, 0.5);
}
</style>