<script setup>
import {RouterView, RouterLink} from 'vue-router'
import NavBar from "@/components/NavBar";
</script>

<template>
  <NavBar/>
  <div class="main">
    <RouterView/>
  </div>
</template>

<style>
.main {
  /*outline: 3px solid purple;*/
  position: relative;
  margin-top: 75px;
  width: 100%;
}
</style>