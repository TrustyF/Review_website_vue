<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import {clickOutSide as vClickOutSide} from '@mahdikhashan/vue3-click-outside'
import {disableBodyScroll, enableBodyScroll, clearAllBodyScrollLocks} from 'body-scroll-lock';
import EditMaster from "@/components/MediaContainer/Editor/EditMaster.vue";

let props = defineProps(["test"]);
const curr_api = inject("curr_api");

const edit_media = inject("edit_media");
let is_open = ref(false)

async function close() {
  if (is_open.value === true) {
    let pane = document.getElementById('edit_pane')
    let main = document.getElementById('main')

    pane.classList.add('hidden')
    enableBodyScroll(main)

    await new Promise(resolve => setTimeout(resolve, 100));
    edit_media.value = undefined
    await new Promise(resolve => setTimeout(resolve, 10));
    is_open.value = false
  }
}

async function open() {
  console.log(is_open.value)
  if (is_open.value === false) {
    let pane = document.getElementById('edit_pane')
    let main = document.getElementById('main')

    pane.classList.remove('hidden')
    disableBodyScroll(main)

    await new Promise(resolve => setTimeout(resolve, 100));
    is_open.value = true

  }
}

watch(edit_media, (oldV, newV) => {
  open()
})
onMounted(() => {
  open()
})
</script>

<template>
  <div class="base hidden" id="edit_pane">
    <div class="background" @click="close"></div>
    <edit-master v-if="edit_media!==undefined"></edit-master>
  </div>
</template>

<style scoped>
.base {
  inset: 0;
  padding: 10px;
  z-index: 50;
  position: fixed;
  background: rgba(0, 0, 0, 0.9);
  transition: 100ms ease-in-out;
  display: grid;
  align-items: center;
}

.hidden {
  opacity: 0;
  visibility: hidden;
}

.background {
  position: fixed;
  width: 100%;
  height: 100%;
  inset: 0;
  z-index: 15;
  content: "";
}
</style>