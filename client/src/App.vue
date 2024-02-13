<script setup>
// import {inject, onMounted} from 'vue'
import {RouterView} from 'vue-router'
import NavBar from "@/components/General/NavBar.vue";
import '@/assets/styles/globals.css'
import '@/assets/styles/dark.css'
import {computed, inject, onMounted, provide, ref, watch} from "vue";
import TooltipBadge from "@/components/tooltip/tooltipBadge.vue";
import TooltipEditor from "@/components/tooltip/tooltipEditor.vue";
import TooltipMediaDetails from "@/components/tooltip/tooltipMediaDetails.vue";

const selected_media = ref({})
const edit_media = ref(undefined)
const edit_mode = inject('edit_mode')
const edit_pane_open = ref(false)
const add_pane_open = ref(false)
const media_detail_pane_open = ref(false)
let is_mobile = ref(false)
let is_visible_navbar = ref(false)

const media_scales = computed(() => {
  return {
    'movie': {
      'size': [500, 750],
      'scale': !is_mobile.value ? 0.35 : 0.2,
    },
    'tv': {
      'size': [500, 750],
      'scale': !is_mobile.value ? 0.35 : 0.2,
    },
    'manga': {
      'size': [256, 360],
      'scale': !is_mobile.value ? 0.7 : 0.5,
    },
    'youtube': {
      'size': [1280, 720],
      'scale': !is_mobile.value ? 0.2 : 0.14,
    },
    'game': {
      'size': [264, 352],
      'scale': !is_mobile.value ? 0.69 : 0.5,
    },
  }
})

provide('selected_media', selected_media)
provide('edit_media', edit_media)
provide('edit_pane_open', edit_pane_open)
provide('add_pane_open', add_pane_open)
provide('media_detail_pane_open', media_detail_pane_open)
provide('is_mobile', is_mobile)
provide('is_visible_navbar', is_visible_navbar)
provide('media_scales', media_scales)

const curr_api = inject("curr_api");

function check_mobile() {
  // is_mobile.value = document.body.clientWidth < 724;
  is_mobile.value = document.body.clientWidth <= 500;
}

function move_sticky_elements_with_nav(nav_vis) {
  let stickies = document.getElementsByClassName('sticky_nav')

  Array.from(stickies).forEach((elem) => {
    if (nav_vis) {
      elem.style.transitionDelay = '0ms'
      elem.style.top = '80px'

    } else {
      elem.style.transitionDelay = '250ms'
      elem.style.top = '10px'
    }
  })

}

watch(is_visible_navbar, (oldV, newV) => {
  move_sticky_elements_with_nav(newV)
})

onMounted(() => {
  check_mobile()
  addEventListener("resize", () => check_mobile())
})

</script>
<template>
  <tooltip-badge></tooltip-badge>

  <NavBar/>
  <div class="tooltip_editor_top_wrapper" v-if="edit_pane_open && edit_mode">
    <tooltip-editor :edit="true"></tooltip-editor>
  </div>

  <div class="tooltip_editor_top_wrapper" v-if="media_detail_pane_open">
    <tooltip-media-details></tooltip-media-details>
  </div>

  <button v-if="edit_mode && curr_api!=='http://192.168.1.11:5000'" style="position: fixed;right: 10px;top: 70px;z-index: 10" @click="add_pane_open=true">add</button>
  <p v-if="edit_mode" style="position: fixed;right: 10px;top: 150px;font-size: 0.7em;z-index: 10;background-color: black">{{ curr_api }}</p>

  <div class="tooltip_editor_top_wrapper" v-if="add_pane_open && edit_mode">
    <tooltip-editor :add="true"></tooltip-editor>
  </div>

  <div class="main" id="main">
    <RouterView>
    </RouterView>
  </div>

</template>

<style scoped>
.main {
  position: relative;

  margin: 0 auto 0 auto;
  max-width: 1000px;
  min-height: 80vh;
  /*overflow-x: clip;*/

  padding: 0 40px 0 40px;
}

.tooltip_editor_top_wrapper {
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;

  padding: 25px;
  /*inset: 0;*/
  /*height: 100%;*/
  /*width: 100%;*/

  position: fixed;
  z-index: 30000;
  background-color: rgba(15, 15, 15, 97%);
}

@media only screen and (max-width: 500px) {
  .main {
    padding: 0 5px 0 5px;
    overflow-x: clip;
  }
}
</style>
