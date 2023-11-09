<script setup>
import {RouterLink} from "vue-router";
import logo from '@/assets/ui/logo.png'
import {inject, onMounted, ref} from 'vue'

let editMode = inject('editMode')
let prev_scroll = ref(0)

function activate_edit_mode() {
  editMode.value = !editMode.value
}

function get_scroll_direction(event) {
  const nav = document.getElementById('navbar')

  if (prev_scroll.value > window.scrollY) {
    nav.classList.remove('hidden')
  } else if (prev_scroll.value < window.scrollY) {
    nav.classList.add('hidden')
  }
  prev_scroll.value = window.scrollY;
}

onMounted(() => {
  addEventListener('scroll', event => get_scroll_direction())
})
</script>

<template>
  <nav class="dark_accent navbar" id="navbar">
    <div class="wrapper">
      <img :src="logo" alt="website icon" style="height: 40px">
      <RouterLink active-class="active" class="link" to="/">Home</RouterLink>
      <h1>|</h1>
      <RouterLink active-class="active" class="link" to="/movies">Movies</RouterLink>
      <RouterLink active-class="active" class="link" to="/series">Series</RouterLink>
      <h1>•</h1>
      <RouterLink active-class="active" class="link" to="/anime">Anime</RouterLink>
      <RouterLink active-class="active" class="link" to="/manga">Manga</RouterLink>
      <h1>•</h1>
      <RouterLink active-class="active" class="link" to="/games">Games</RouterLink>
    </div>
    <div class="edit_button" @click="activate_edit_mode"></div>
  </nav>


</template>

<style scoped>
.navbar {
  outline: 1px solid red;
  /*background-color: rgba(0, 0, 0, 1);*/
  display: flex;
  align-items: center;
  justify-content: flex-start;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 5;

  height: 70px;
  font-size: 1.2em;

  transition: 250ms;
  transition-delay: 0ms;
}

.hidden {
  transform: translate(0,-100%);
  transition-delay: 250ms;
}

nav ul li {
  list-style: none;
  display: inline-block;
  margin-right: 3vh;
  color: white;
}

.edit_button {
  position: absolute;
  right: 0;
  width: 50px;
  height: 100%;
  /*outline: 1px solid red;*/
}

.wrapper {
  display: flex;
  flex-flow: row nowrap;
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