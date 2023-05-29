<script setup>
import {ref, onMounted, inject} from 'vue'
let darkMode = inject('darkMode')

let test = {
  "mood": {
    "chill": {},
    "upbeat":{},
    "depressing":{},
    "exciting":{},
    "smart":{},
  }
}
let num_buttons = Array(5)

function distribute_buttons_circle() {
  let buttons = document.getElementsByClassName('select_button')
  let wrapper = document.getElementById("selector_wrapper")
  let w_box = wrapper.getBoundingClientRect()
  let box_center = [(w_box.left + w_box.right) / 2, (w_box.top + w_box.bottom) / 2]

  let spacing = wrapper.offsetWidth/2

  let angle = Math.PI / (buttons.length / 2);
  let offset = 0
  let speed = 0.01

  let timer = setInterval(function () {
    if (timer===undefined) clearInterval(timer)
    offset += 1
    draw(offset)
  }, 16)

  // draw()

  function draw(offset) {
    for (let i = 0; i < buttons.length; i++) {
      let x = Math.cos(angle * i + (offset * speed)) * spacing
      let y = Math.sin(angle * i + (offset * speed)) * spacing

      buttons[i].style.left = x + box_center[0] + 'px'
      buttons[i].style.top = y + box_center[1] + 'px'
    }
  }
}

onMounted(() => {
  distribute_buttons_circle()
})
</script>

<template>
  <div class="wrapper">
    <h1>What are you in the mood for ?</h1>
    <div id="selector_wrapper" v-for="category in test" :key="category">
      <div :class="darkMode ? 'select_button dark_accent' : 'select_button'" v-for="(elem,i) in Object.keys(category)" :key="i">{{ elem.toUpperCase() }}</div>
    </div>
  </div>
</template>

<script>

</script>

<style scoped>
.wrapper {
  /*outline: 1px solid blue;*/
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
  transform: translate(-50%, -50%);

  cursor: pointer;

  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 1);
  font-weight: bold;

  display: flex;
  justify-content: center;
  align-items: center;
}
</style>