<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import Badge from "@/components_V2/media_container/movie_container/badge.vue";

let props = defineProps(["data", "title"]);
let emits = defineEmits(["id"]);
const curr_api = inject("curr_api");

let checked_ids = []

function clear_checkboxes() {
  let checkboxes = document.getElementsByClassName('checkbox')
  Array.from(checkboxes).forEach((elem) => {
    if (elem.id.includes(props['title'])) {
      elem.checked = false
    }
  })
  checked_ids = []
  emits('id', checked_ids)

}

function toggle_checkbox(id) {
  let checkbox = document.getElementById(`checkbox${id}${props['title']}`)

  if (checkbox.checked) {
    checkbox.checked = false
    let index = checked_ids.indexOf(id)
    checked_ids.splice(index,1)
  } else {
    checkbox.checked = true
    checked_ids.push(id)
  }
  emits('id', checked_ids)

}

</script>

<template>
  <div class="filter_wrapper">
    <h1>{{ title }}</h1>
    <button @click="clear_checkboxes">Clear</button>

    <div class="filter_list">

      <div class="filter_box" v-for="range in data" :key="range">
        <input class="range" :id="`range${range}${title}`" type="range"
        min="ra">

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