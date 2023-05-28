<script setup>
import {inject} from 'vue'
import {RouterView, RouterLink} from 'vue-router'
import NavBar from "@/components/NavBar";
import './styles/globals.css'
import './styles/dark.css'

let darkMode = inject("darkMode")

</script>

<template>
  <div :class="darkMode ? 'main dark' : 'main white'">
    <NavBar/>
    <RouterView/>
  </div>
</template>
<style scoped>
.main {
  transition: 500ms;
}
.white {
  background-color: white;
}
</style>