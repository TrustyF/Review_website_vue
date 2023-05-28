<script setup>
import {RouterLink} from "vue-router";
import logo from '/public/assets/ui/logo.png'

</script>

<template>
  <nav class="dark_accent">
    <div class="wrapper">
      <img :src="logo" alt="website icon" style="height: 30px">
      <RouterLink active-class="active" class="link" to="/movies">Movies</RouterLink>
      <RouterLink active-class="active" class="link" to="/series">Series</RouterLink>
      <RouterLink active-class="active" class="link" to="/manga">Manga</RouterLink>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar"
}
</script>

<style scoped>
nav {
  /*background-color: rgba(0, 0, 0, 1);*/
  display: flex;
  align-items: center;
  position: relative;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
  transition: top 0.2s linear;
  height: 50px;
  font-size: 1em;
}

nav ul li {
  list-style: none;
  display: inline-block;
  margin-right: 3vh;
  color: white;
}

.wrapper {
  display: flex;
  flex-flow: row;
  justify-content: flex-start;
  align-items: center;
  margin: 10px;
  gap: 20px;
}
.link {
  font-weight: lighter;
}
.link, link:visited {
  text-decoration: none;
  color: white;
}
.active {
  font-weight: bold;
}
</style>