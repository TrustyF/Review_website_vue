<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import Badge from "@/components_V2/media_container/movie_container/badge.vue";

let props = defineProps(["data", "title"]);
let emits = defineEmits(["id"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="filter_wrapper">
    <h1>{{ title }}</h1>

    <div class="filter_list">

      <div class="filter_box" v-for="filter in data" :key="filter['id']">
        <input id="checkbox" type="checkbox" @change="emits('id',filter['id'])" >

        <badge v-if="filter['image_path']!==undefined" :data="filter" :min_size="170" :show_title="true"></badge>
        <label v-else for="checkbox">{{ filter['name'] }}</label>
      </div>

    </div>
  </div>
</template>

<style scoped>
.filter_wrapper {
  display: flex;
  flex-flow: column;
  gap: 5px;
  outline: 1px solid red;
}
.filter_list {
  overflow-y: scroll;
  display: flex;
  flex-flow: column;
  gap: 5px;
}
.filter_box {
  /*outline: 1px solid greenyellow;*/
  display: flex;
  flex-flow: row;

  align-items: center;
  gap: 5px;

}
.filter_image {
  height: 30px;
}
</style>