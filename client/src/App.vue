<script setup>
// import {inject, onMounted} from 'vue'
import {RouterView} from 'vue-router'
import NavBar from "@/components/General/NavBar.vue";
import '@/assets/styles/globals.css'
import '@/assets/styles/dark.css'
import CreditsFooter from "@/components/General/CreditsFooter.vue";
import {onMounted, provide, ref, watch} from "vue";
import TooltipBadge from "@/components/tooltip/tooltipBadge.vue";
import EditPage from "@/pages/EditPage.vue";

const selected_media = ref({})
const edit_media = ref(undefined)
const edit_mode = ref(true)
const edit_pane_open = ref(false)
let is_mobile = ref(false)
let is_visible_navbar = ref(false)

provide('selected_media', selected_media)
provide('edit_media', edit_media)
provide('edit_mode', edit_mode)
provide('edit_pane_open', edit_pane_open)
provide('is_mobile', is_mobile)
provide('is_visible_navbar', is_visible_navbar)

function check_mobile() {
  is_mobile.value = document.body.clientWidth < 500;
}

onMounted(() => {
  check_mobile()
  addEventListener("resize", () => check_mobile())
})

watch(is_visible_navbar, (oldVal, newVal) => {
  let main = window.document.getElementById('main')
  if (newVal) {
    main.classList.add('navbar_offset')
  } else {
    main.classList.remove('navbar_offset')
  }
})

</script>
<template>
  <tooltip-badge></tooltip-badge>

  <NavBar/>
  <div class="edit_page_top_wrapper" v-if="edit_pane_open">
    <edit-page></edit-page>
  </div>

  <div class="main navbar_offset" id="main">
    <RouterView>
    </RouterView>
    <CreditsFooter/>
  </div>

</template>

<style scoped>
.main {
  position: relative;

  margin: 0 auto 0 auto;
  max-width: 1000px;
  min-height: 80vh;

  padding: 0 10px 0 10px;
  transition: transform 250ms;
  transition-delay: 250ms;
}

.edit_page_top_wrapper {

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

.navbar_offset {
  transform: translate(0, 60px);
  transition-delay: 0ms;
}

@media only screen and (max-width: 724px) {
  .navbar_offset {
    transform: translate(0, 100px);
    transition-delay: 0ms;
  }
}
</style>
