<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import Badge from "@/components/media_container/movie_container/sub_components/badge.vue";

let props = defineProps(["data", "title", "step", "time"]);
let emits = defineEmits(["values"]);
const curr_api = inject("curr_api");

let min_max = computed(() => [props['data'][0], props['data'][1]])
let min_range = ref(props['data'][0])
let max_range = ref(props['data'][1])

let is_changed = ref(false)

function clear_ranges() {
  min_range.value = props['data'][0]
  max_range.value = props['data'][1]
  emit_ranges()
}

function emit_ranges() {
  is_changed.value = true
  emits('values', [min_range.value, max_range.value])
}

function reset() {
  clear_ranges()
  setTimeout(() => is_changed.value = false, 0.1)
}

function convert_seconds_to_time(f_seconds) {
  let minutes = f_seconds % 60
  let hours = (f_seconds - minutes) / 60

  if (hours < 1) return minutes + ' min'
  return hours + 'h ' + minutes;
}
</script>

<template>
  <div class="filter_wrapper" v-if="data !== undefined">


    <div class="title">
      <h1>{{ title }}</h1>
      <img v-if="is_changed" src="/src/assets/ui/rewind.png" style="filter: brightness(1000%)" class="clear" alt="clear"
           @click="reset">
    </div>
    <div style="border-bottom: 1px solid white;margin-top: 2px"></div>

    <div class="filter_list">
      <div class="range_box">

        <label v-if="time" class="label" for="range_min">{{ convert_seconds_to_time(min_range) }}</label>
        <label v-else class="label" for="range_min">{{ min_range }}</label>

        <input v-model="min_range" class="slider" type="range" id="range_min"
               :min="min_max[0]" :max="min_max[1]" :step="step" @change="emit_ranges">
      </div>
      <div class="range_box">

        <label v-if="time" class="label" for="range_max">{{ convert_seconds_to_time(max_range) }}</label>
        <label v-else class="label" for="range_max">{{ max_range }}</label>

        <input v-model="max_range" class="slider" type="range" id="range_max"
               :min="min_max[0]" :max="min_max[1]" :step="step" @change="emit_ranges">
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

  max-height: 100%;
  width: 100%;
}

.filter_list {
  display: flex;
  flex-flow: column;
}

.title {
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;
  align-items: center;
  gap: 5px;
}

.range_box {
  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
}

.label {
  text-align: center;
  width: 3em;
  font-size: 0.8em;
}

.slider {
  width: 100%;
}

.clear {
  height: 1em;
  filter: invert();
  cursor: pointer;
}
</style>