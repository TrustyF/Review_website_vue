<script setup>
// import {inject, onMounted} from 'vue'
import {RouterView} from 'vue-router'
import NavBar from "@/components/General/NavBar.vue";
import '@/assets/styles/globals.css'
import '@/assets/styles/dark.css'
import CreditsFooter from "@/components/General/CreditsFooter.vue";
import {onMounted, provide, ref} from "vue";
import MediaPane from "@/components/MediaContainer/Pane/MediaPane.vue";



const selected_media = ref(undefined)

provide('selected_media', selected_media)

</script>

<template>
  <NavBar/>
  <div class="main" id="main">
    <media-pane></media-pane>
    <RouterView/>
    <CreditsFooter/>
  </div>
</template>

<style scoped>
.main {
  /*outline: 1px solid red;*/
  max-width: 1000px;
  margin: 75px auto 0 auto;
  padding: 0 20px 0 20px;
}

@media only screen and (max-width: 647px) {
  .main {
    margin: 110px auto 0 auto;
  }
}
</style>
