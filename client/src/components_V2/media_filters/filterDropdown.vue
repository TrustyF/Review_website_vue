<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import Badge from "@/components_V2/media_container/movie_container/badge.vue";

let props = defineProps(["data", "title"]);
let emits = defineEmits(["id"]);
const curr_api = inject("curr_api");

function clear_checkboxes() {
  let checkboxes = document.getElementsByClassName('checkbox')
  Array.from(checkboxes).forEach((elem) => {
    if (elem.id.includes(props['title'])) {
      elem.checked = false
    }
  })
}

function toggle_checkbox(id) {
  let checkbox = document.getElementById(`checkbox${id}${props['title']}`)

  if (checkbox.checked) {
    checkbox.checked = false
    emits('id', [id,false])
  } else {
    checkbox.checked = true
    emits('id', [id,true])

  }
}

</script>

<template>
  <div class="filter_wrapper">
    <h1>{{ title }}</h1>
    <button @click="clear_checkboxes">Clear</button>

    <div class="filter_list">

      <div class="filter_box" v-for="filter in data" :key="filter['id']">
        <input class="checkbox" :id="`checkbox${filter['id']}${title}`" type="checkbox">

        <badge v-if="filter['image_path']!==undefined" :data="filter" :min_size="170"
               :show_title="true"></badge>
        <label v-else>{{ filter['name'] }}</label>
        <div class="checkbox_click_box" @click="toggle_checkbox(filter['id'])"></div>

      </div>

    </div>
  </div>
</template>

<style scoped>
.filter_wrapper {
  position: relative;
  display: flex;
  flex-flow: column;
  gap: 5px;
  /*outline: 1px solid red;*/
  padding: 10px;
  border: 1px solid #969696;
}

.filter_list {
  overflow-y: scroll;
  display: flex;
  flex-flow: column;
}

.filter_box {
  position: relative;
  display: flex;
  flex-flow: row;

  align-items: center;
  gap: 5px;
  padding: 5px 0 5px 0;
}

.filter_image {
  height: 30px;
}

.checkbox_click_box {
  /*outline: 1px solid greenyellow;*/
  position: absolute;
  width: 100%;
  height: 100%;
}
</style>