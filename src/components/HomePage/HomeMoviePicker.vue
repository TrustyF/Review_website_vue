<script setup>
import {ref, onMounted, onUnmounted, inject} from 'vue'

let darkMode = inject('darkMode')

let test = {
  "mood": {
    "chill": {},
    "smart": {},
    "scary": {},
    "funny": {},

  }
}
let num_buttons = Array(5)
let w_box

function calc_bounding_box() {
  w_box = document.getElementById("selector_wrapper").getBoundingClientRect()
}

onMounted(() => {
  calc_bounding_box()
  window.addEventListener('resize', calc_bounding_box)
})
onUnmounted(() => {
  window.removeEventListener('resize', calc_bounding_box)
})
</script>

<template>
  <div class="picker_wrapper">
    <h1>What are you in the mood for ?</h1>
    <div id="selector_wrapper" v-for="category in test" :key="category">
      <div :class="darkMode ? 'select_button dark_accent' : 'select_button'" v-for="(elem,i) in Object.keys(category)"
           :key="i">{{ elem.toUpperCase() }}
      </div>
    </div>
  </div>

</template>

<style scoped>
.picker_wrapper {
  outline: 1px solid blue;
  /*width: 80%;*/
  /*padding: 10px;*/
  /*margin: auto;*/
}

#selector_wrapper {
  outline: 1px green solid;
  width: 300px;
  height: 300px;
  margin: auto;
}

.select_button {
  position: absolute;
  padding: 10px 20px 10px 20px;

  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);

  cursor: pointer;

  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 1);
  font-weight: bold;

  display: flex;
  justify-content: center;
  align-items: center;

  /*transition: 16ms ease-in-out;*/
}
</style>