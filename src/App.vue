<script setup>
// import {inject, onMounted} from 'vue'
import {RouterView} from 'vue-router'
import NavBar from "@/components/General/NavBar.vue";
import '@/assets/styles/globals.css'
import '@/assets/styles/dark.css'
import {inject, onMounted, provide, ref, watch} from "vue";
import TooltipBadge from "@/components/tooltip/tooltipBadge.vue";
import TooltipEditor from "@/components/tooltip/tooltipEditor.vue";
import {check_server_awake} from "@/utils.js";

const selected_media = ref({})
const edit_media = ref(undefined)
const edit_mode = inject('edit_mode')
const edit_pane_open = ref(false)
const add_pane_open = ref(false)
let is_mobile = ref(false)
let is_visible_navbar = ref(false)

provide('selected_media', selected_media)
provide('edit_media', edit_media)
provide('edit_pane_open', edit_pane_open)
provide('add_pane_open', add_pane_open)
provide('is_mobile', is_mobile)
provide('is_visible_navbar', is_visible_navbar)

const curr_api = inject("curr_api");

function check_mobile() {
  is_mobile.value = document.body.clientWidth < 500;
}

function ping_server(){
  check_server_awake(curr_api)
}

onMounted(() => {
  ping_server()
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

  <button v-if="edit_mode" style="position: absolute;right: 10px;top: 70px" @click="add_pane_open=true">add</button>
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
  /*outline: 1px solid orange;*/
  position: relative;

  margin: 0 auto 0 auto;
  max-width: 1000px;
  min-height: 80vh;

  padding: 0 10px 0 10px;

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
</style>
