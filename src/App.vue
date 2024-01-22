<script setup>
// import {inject, onMounted} from 'vue'
import {RouterView} from 'vue-router'
import NavBar from "@/components/General/NavBar.vue";
import '@/assets/styles/globals.css'
import '@/assets/styles/dark.css'
import CreditsFooter from "@/components/General/CreditsFooter.vue";
import {onMounted, provide, ref, watch} from "vue";
import TooltipBadge from "@/components/tooltip/tooltipBadge.vue";

const selected_media = ref(undefined)
const edit_media = ref(undefined)
const edit_mode = ref(true)
let is_mobile = ref(false)
let is_visible_navbar = ref(false)

provide('selected_media', selected_media)
provide('edit_media', edit_media)
provide('edit_mode', edit_mode)
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
  if (newVal){
    main.classList.add('navbar_offset')
  } else {
    main.classList.remove('navbar_offset')
  }
})

</script>
<template>
  <tooltip-badge></tooltip-badge>

  <NavBar/>
  <div class="main navbar_offset" id="main">
    <RouterView/>
    <CreditsFooter/>
  </div>
</template>

<style scoped>
.main {
  /*outline: 1px solid red;*/

  margin: 0 auto 0 auto;
  max-width: 1000px;
  min-height: 80vh;

  padding: 0 10px 0 10px;
  transition: transform 250ms;
  transition-delay: 250ms;
}
.navbar_offset{
  transform: translate(0,60px);
  transition-delay: 0ms;
}
@media only screen and (max-width: 724px) {
  .navbar_offset{
    transform: translate(0,100px);
    transition-delay: 0ms;
  }
}
</style>
