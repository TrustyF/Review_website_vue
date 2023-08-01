<script setup>
import {RouterLink} from "vue-router";
import logo from '@/assets/ui/logo.png'

</script>

<template>
  <nav class="dark_accent">
    <div class="wrapper">
      <img :src="logo" alt="website icon" style="height: 40px">
      <RouterLink active-class="active" class="link" to="/movie_picker">Home</RouterLink>
      <h1>|</h1>
      <RouterLink active-class="active" class="link" to="/movies">Movies</RouterLink>
      <RouterLink active-class="active" class="link" to="/series">Series</RouterLink>
      <h1>•</h1>
      <RouterLink active-class="active" class="link" to="/anime">Anime</RouterLink>
      <RouterLink active-class="active" class="link" to="/manga">Manga</RouterLink>
      <h1>•</h1>
      <RouterLink active-class="active" class="link" to="/games">Games</RouterLink>
    </div>
  </nav>


</template>

<style scoped>
nav {
  /*outline: 1px solid red;*/
  /*background-color: rgba(0, 0, 0, 1);*/
  display: flex;
  align-items: center;
  justify-content: flex-start;
  position: relative;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
  transition: top 0.2s linear;
  height: 70px;
  font-size: 1.2em;
}

nav ul li {
  list-style: none;
  display: inline-block;
  margin-right: 3vh;
  color: white;
}

.wrapper {
  /*outline: 1px solid blue;*/
  display: flex;
  flex-flow: row;
  align-items: center;
  width: 80%;
  margin: auto;
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
  text-decoration: underline;
}
</style>