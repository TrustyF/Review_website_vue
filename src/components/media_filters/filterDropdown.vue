<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import Badge from "@/components/media_container/movie_container/sub_components/badge.vue";
import {log_event} from "@/scripts/log_events";

let props = defineProps(["data", "title"]);
let emits = defineEmits(["id"]);
const curr_api = inject("curr_api");

let checked_ids = ref([])
let is_changed = ref(false)

function clear_checkboxes() {
  let checkboxes = document.getElementsByClassName('checkbox')
  Array.from(checkboxes).forEach((elem) => {
    if (elem.id.includes(props['title'])) {
      elem.checked = false
    }
  })
  checked_ids.value = []
  emits('id', checked_ids)

}

function toggle_checkbox(id) {
  let checkbox = document.getElementById(`checkbox${id}${props['title']}`)

  if (checkbox.checked) {
    checkbox.checked = false
    let index = checked_ids.value.indexOf(id)
    checked_ids.value.splice(index, 1)
  } else {
    checkbox.checked = true
    checked_ids.value.push(id)
  }
  emits('id', checked_ids)
  is_changed.value = true
}

function log_use(filter) {
  log_event('filter_use', 'int', [props.title, filter['name']])
}

function reset() {
  clear_checkboxes()
  setTimeout(() => is_changed.value = false, 0.1)
}

</script>

<template>
  <div class="filter_wrapper" v-if="data !== undefined">

    <div class="title">
      <h1>{{ title }}</h1>
      <div v-if="checked_ids.length > 0" style="filter: brightness(1000%)" class="clear bi-arrow-counterclockwise"
           @click="reset"/>
    </div>
    <div style="border-bottom: 1px solid white;margin-top: 2px"></div>

    <div class="filter_list">

      <div class="filter_box" v-for="filter in data" :key="filter['id']">
        <input class="checkbox" :id="`checkbox${filter['id']}${title}`" type="checkbox">

        <badge v-if="filter['image_path']!==undefined" :data="filter" :min_size="170"
               :show_title="true"></badge>
        <label class="label" v-else>{{ filter['name'] }}</label>
        <div class="checkbox_click_box" @click="toggle_checkbox(filter['id']);log_use(filter)"></div>

      </div>

    </div>
  </div>
</template>

<style scoped>
.filter_wrapper {
  position: relative;
  display: flex;
  flex-flow: column nowrap;
  gap: 5px;
  /*outline: 1px solid red;*/
  max-height: 400px;
  height: auto;
  /*border: 1px solid white;*/
  padding: 20px;
  background-color: #131215;
  filter: drop-shadow(1px 1px 3px black);
  border-radius: 10px;
}

.filter_list {
  overflow-y: scroll;
  overflow-x: hidden;
  display: flex;
  flex-flow: column nowrap;
}

.filter_box {
  position: relative;
  display: flex;
  flex-flow: row;
  align-items: center;
  gap: 5px;
  padding: 5px;
}

.title {
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;
  align-items: center;
  gap: 5px;
}

.clear {
  font-size: 1em;
  cursor: pointer;
}

.label {
  font-size: 0.8em;
  max-width: 10em;
  /*white-space: nowrap;*/
  /*text-overflow: ellipsis;*/
  /*overflow-x: hidden;*/
  /*overflow-y: auto;*/
}

.checkbox_click_box {
  /*outline: 1px solid greenyellow;*/
  position: absolute;
  width: 100%;
  height: 100%;
}
</style>