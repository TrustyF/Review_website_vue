<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import FilterContainer from "../media_filters/filterContainer.vue";
import FilterSearch from "../media_filters/filterSearch.vue";
import {clickOutSide as vClickOutSide} from '@mahdikhashan/vue3-click-outside'

let props = defineProps(["media_type"]);
let emits = defineEmits(["filter"]);
const curr_api = inject("curr_api");

let filter_container = ref()
let is_filter_box_open = ref(false)
let box_height = ref('0px')

function emit_filter(event) {
  emits('filter', event)
}

function calculate_box_height() {
  let box = filter_container.value.getBoundingClientRect()

  let bottom = (window.scrollY + window.innerHeight) - box.top - 100

  box_height.value = String(bottom) + 'px'
}

function toggle_filters_box() {
  let classes = filter_container.value.classList

  if (classes.contains('visible')) {
    classes.remove('visible')
    is_filter_box_open.value = false
  } else {
    calculate_box_height()
    classes.add('visible')
    setTimeout(() => is_filter_box_open.value = true, 1)
  }
}

function close_filters_box() {
  let classes = filter_container.value.classList

  if (!is_filter_box_open.value) return

  console.log('closing')
  classes.remove('visible')
  is_filter_box_open.value = false

}

onMounted(() => {
  calculate_box_height()
})
</script>

<template>
  <div class="filters_top_container">

    <div class="filters_box">
      <img alt="filters" @click="toggle_filters_box" class="filter_button"
           src="src/assets/ui/filter_button.png">
      <filter-search @filter="emit_filter(['search',$event])"></filter-search>
    </div>

    <div ref="filter_container" class="filter_wrapper" v-click-out-side="close_filters_box">
      <div class="overflow_filter">
        <filter-container @filter="emit_filter" :media_type="media_type"></filter-container>
      </div>
      <div class="filter_wrapper_arrow"></div>
      <div class="filter_wrapper_arrow_border"></div>
    </div>

  </div>
</template>

<style scoped>
.filters_top_container {
  position: sticky;
  z-index: 100;
  top: 10px;
  /*width: 90%;*/
  display: flex;
  flex-flow: row nowrap;
  justify-content: center;
}

.filters_box {
  /*outline: 1px solid red;*/
  position: absolute;
  height: 35px;
  width: 0;

  display: flex;
  flex-flow: row nowrap;

  justify-content: center;
  /*align-items: center;*/
  align-content: flex-start;

  gap: 10px;
}

.filter_button {
  height: auto;
  background-color: #d7d7c5;
  padding: 7px;
  border-radius: 30%;
  filter: invert();
  box-shadow: 1px 1px 5px white;
  cursor: pointer;
  z-index: 10;
  object-fit: contain;
  border: 2px solid #969696;
}

.filter_wrapper {
  position: absolute;
  padding: 10px;
  margin-top: 80px;
  border-radius: 20px;
  filter: drop-shadow(10px 10px 5px black);
  border: 3px solid #969696;
  max-height: v-bind(box_height);

  width: 95vw;

  visibility: hidden;
  opacity: 0;
  transform: translate(0, -50px);
  transition: 500ms ease-in-out;
  background: linear-gradient(to bottom, #2c2c40 50%, #25222a 100%);
}

.visible {
  visibility: visible;
  opacity: 100%;
  transform: translate(0, 0);
  transition: 200ms ease-in-out;
}

.overflow_filter {
  max-height: v-bind(box_height);
  overflow-y: scroll;
  border-radius: 20px;
}

.filter_wrapper_arrow {
  content: "";
  position: absolute;
  z-index: 10;
  top: -40px;
  left: 50%;
  margin-left: -20px;
  border-width: 20px;
  border-style: solid;
  border-color: transparent transparent #2c2c40 transparent;
}

.filter_wrapper_arrow_border {
  content: "";
  position: absolute;
  z-index: 5;
  top: -47px;
  left: 50%;
  margin-left: -23px;
  border-width: 23px;
  border-style: solid;
  border-color: transparent transparent #969696 transparent;
}
</style>