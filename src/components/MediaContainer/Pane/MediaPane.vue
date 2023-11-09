<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaExpanded from "@/components/MediaContainer/Master/Expanded/MediaExpanded.vue";
import {clickOutSide as vClickOutSide} from '@mahdikhashan/vue3-click-outside'
import x_button from '@/assets/ui/x_button.png'

let props = defineProps(["test"]);
const curr_api = inject("curr_api");

const selected_media = inject("selected_media");
let is_open = ref(false)


async function close() {
  if (is_open.value === true) {
    let pane = document.getElementById('media_pane')

    pane.classList.add('hidden')

    await new Promise(resolve => setTimeout(resolve, 200));
    selected_media.value = undefined
    await new Promise(resolve => setTimeout(resolve, 10));
    is_open.value = false
  }
}

async function open() {
  console.log(is_open.value)
  if (is_open.value === false) {
    let pane = document.getElementById('media_pane')

    pane.classList.remove('hidden')
    await new Promise(resolve => setTimeout(resolve, 200));
    is_open.value = true
  }
}

watch(selected_media, (oldV, newV) => {
  open()
})

</script>

<template>

  <div class="media_pane_wrapper hidden" id="media_pane">
    <div class="feed" v-click-out-side="close">
      <img :src="x_button" alt="close_button" class="close_button" @click="close">
      <media-expanded :data="selected_media" v-if="selected_media!==undefined"></media-expanded>
    </div>
  </div>

</template>

<style scoped>
.media_pane_wrapper {
  inset: 0;
  margin: auto;
  position: fixed;
  width: 100%;
  height: 100%;
  z-index: 50;
  background-color: rgba(0, 0, 0, 0.9);

  transition: 200ms ease-in-out;
}

.feed {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  height: 40%;
  /*min-height: 300px;*/
  position: absolute;
  inset: 25px;
  max-width: 1000px;
  margin: auto;
  padding: 15px;
  border-radius: 10px;
  background: #1c1b23;
  outline: 2px solid #464646;
}
.close_button {
  position: absolute;
  right: 5px;
  top: 5px;
  width: 25px;
  height: 25px;
  filter: invert() opacity(50%);
  cursor: pointer;
}

.hidden {
  /*transform: translate(0, 20%);*/
  opacity: 0;
  visibility: hidden;
}

@media only screen and (max-width: 500px) {
  .feed {
    height: 95%;
    padding: 25px;
  }
}
</style>