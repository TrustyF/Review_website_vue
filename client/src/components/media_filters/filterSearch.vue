<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let emits = defineEmits(["filter"]);

let is_typing = ref(false)
let last_typed = ref('')

let debounce_id = 0
let throttle_id = 0

function emit_filter(event) {
  emits('filter', event)
}

function throttle_search(text) {
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
    <input class="search_bar" type="text" placeholder="🔍Search"
           @input="throttle_search($event.target.value)"
           @keydown.esc="$event.target.value='';emit_filter('')"
           @keydown.enter="emit_filter($event.target.value)"
           @focus="$event.target.select()">
  </div>
</template>

<style scoped>
.search_bar {
  height: 85%;
  width: 200px;
  outline: none;
  background-color: #131215;
  border: 2px solid grey;
  color: white;
  border-radius: 10px;
  padding: 0 0 0 10px;
}
</style>