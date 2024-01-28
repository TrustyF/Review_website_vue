<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["auto_search"]);
let emits = defineEmits(["filter"]);

let is_typing = ref(false)
let last_typed = ref('')

let debounce_id = 0
let throttle_id = 0

function emit_filter(event) {
  emits('filter', event)
}

function throttle_search(text) {

  if (props['auto_search'] === false) {
    return;
  }

  last_typed.value = text
  clearTimeout(debounce_id)

  debounce_id = setTimeout(() => {
    emit_filter(last_typed.value)
  }, 200)

  if (is_typing.value) return

  is_typing.value = true
  emit_filter(text)

  throttle_id = setTimeout(() => {
    is_typing.value = false
  }, 500)
}

</script>

<template>
  <div>
    <input class="search_bar_wrapper"  type="text" placeholder="🔍Search"
           @input="throttle_search($event.target.value)"
           @keydown.esc="$event.target.value='';emit_filter('')"
           @keydown.enter="emit_filter($event.target.value)"
           @focus="$event.target.select()">
  </div>
</template>

<style scoped>
.search_bar_wrapper {
  /*outline: 1px solid red;*/
  all: unset;
  height: 35px;

  width: 200px;
  background-color: #131215;
  /*background-color: grey;*/
  border: 2px solid grey;
  color: white;
  border-radius: 10px;
  padding: 0 0 0 10px;
}
</style>