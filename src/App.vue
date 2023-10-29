<script setup>
// import {inject, onMounted} from 'vue'
import {RouterView} from 'vue-router'
import NavBar from "@/components/General/NavBar.vue";
import '@/assets/styles/globals.css'
import '@/assets/styles/dark.css'
import CreditsFooter from "@/components/General/CreditsFooter.vue";

</script>

<template>
  <div class="main">
    <NavBar/>
    <RouterView/>
    <CreditsFooter/>
  </div>
</template>

<style scoped>
</style>
