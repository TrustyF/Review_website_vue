<script setup>
import {inject} from 'vue'
import {RouterView, RouterLink} from 'vue-router'
import NavBar from "@/components/General/NavBar";
import './styles/globals.css'
import './styles/dark.css'

let darkMode = inject("darkMode")

</script>

<template>
  <div :class="darkMode ? 'main dark' : 'main white'">
    <NavBar/>
    <div class="app_wrapper">
      <RouterView/>
    </div>
  </div>
</template>
<style scoped>
.app_wrapper {
  /*outline: 1px solid red;*/
  display: block;
  min-height: 100vh;
  margin: auto;
  transition: 500ms;
}
.white {
  background-color: white;
}
</style>