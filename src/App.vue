<script setup>
// import {inject, onMounted} from 'vue'
import {RouterView} from 'vue-router'
import NavBar from "@/components/General/NavBar.vue";
import '@/assets/styles/globals.css'
import '@/assets/styles/dark.css'
import CreditsFooter from "@/components/General/CreditsFooter.vue";
import {onMounted, provide, ref} from "vue";
import MediaPane from "@/components/MediaContainer/Pane/MediaPane.vue";
import EditPane from "@/components/MediaContainer/Pane/EditPane.vue";
import TooltipBadge from "@/components_V2/tooltip/tooltipBadge.vue";

const selected_media = ref(undefined)
const edit_media = ref(undefined)
const edit_mode = ref(true)

provide('selected_media', selected_media)
provide('edit_media', edit_media)
provide('edit_mode', edit_mode)

</script>
<template>
  <tooltip-badge></tooltip-badge>

  <NavBar/>
  <div class="main" id="main">
    <RouterView/>
    <CreditsFooter/>
  </div>
</template>

<style scoped>
.main {
  /*outline: 1px solid red;*/
  max-width: 1000px;
  margin: 75px auto 0 auto;
  padding: 0 10px 0 10px;
}

@media only screen and (max-width: 724px) {
  .main {
    margin: 110px auto 0 auto;
  }
}
</style>
