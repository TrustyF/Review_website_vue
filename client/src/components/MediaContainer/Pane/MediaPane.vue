<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaExpanded from "@/components/MediaContainer/Expanded/Base/MediaExpanded.vue";
import {clickOutSide as vClickOutSide} from '@mahdikhashan/vue3-click-outside'
import { disableBodyScroll, enableBodyScroll, clearAllBodyScrollLocks } from 'body-scroll-lock';

let props = defineProps(["test"]);
const curr_api = inject("curr_api");

const selected_media = inject("selected_media");
let is_open = ref(false)

async function close() {
  if (is_open.value === true) {
    let pane = document.getElementById('media_pane')
    let main = document.getElementById('main')

    pane.classList.add('hidden')
    enableBodyScroll(main)

    await new Promise(resolve => setTimeout(resolve, 100));
    selected_media.value = undefined
    await new Promise(resolve => setTimeout(resolve, 10));
    is_open.value = false
  }
}

async function open() {
  console.log(is_open.value)
  if (is_open.value === false) {
    let pane = document.getElementById('media_pane')
    let main = document.getElementById('main')

    pane.classList.remove('hidden')
    disableBodyScroll(main)

    await new Promise(resolve => setTimeout(resolve, 100));
    is_open.value = true

  }
}

watch(selected_media, (oldV, newV) => {
  open()
})

</script>

<template>
  <div class="base hidden" id="media_pane">
    <div class="background" @click="close"></div>
    <media-expanded :data="selected_media" @closed="close" v-if="selected_media!==undefined"></media-expanded>
  </div>
</template>

<style scoped>
.base {
  /*margin: 10px;*/
  /*outline: 1px solid red;*/
  inset: 0;
  z-index: 50;
  position: fixed;
  background: rgba(0, 0, 0, 0.9);
  transition: 100ms ease-in-out;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hidden {
  opacity: 0;
  visibility: hidden;
}

.background {
  width: 100%;
  height: 100%;
  inset: 0;
  z-index: 15;
  content: "";
}
</style>