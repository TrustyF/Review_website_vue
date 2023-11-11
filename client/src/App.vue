<script setup>
// import {inject, onMounted} from 'vue'
import {RouterView} from 'vue-router'
import NavBar from "@/components/General/NavBar.vue";
import '@/assets/styles/globals.css'
import '@/assets/styles/dark.css'
import CreditsFooter from "@/components/General/CreditsFooter.vue";
import {onMounted, provide, ref} from "vue";

const selected_media = ref(undefined)

provide('selected_media', selected_media)

</script>

<template>
  <div class="main">
    <NavBar/>
    <RouterView/>
    <CreditsFooter/>
  </div>
</template>

<style scoped>
.main {
  outline: 1px solid green;
  max-width: 1000px;
  margin: auto;
}
</style>
