<script setup>
import {RouterLink} from "vue-router";
import logo from '@/assets/ui/logo.png'
import {inject, onMounted, ref} from 'vue'
import LoginBar from "@/components/General/LoginBar.vue";

const curr_api = inject("curr_api");
let edit_mode = inject('edit_mode')
let is_visible_navbar = inject('is_visible_navbar')
let prev_scroll = ref(0)
let nav

function get_scroll_direction(event) {
  // console.log(window.scrollY, document.body.scrollHeight)

  if (window.scrollY === 0) {
    nav.classList.remove('hidden')
    is_visible_navbar.value = false
  } else if (window.innerHeight + Math.round(window.scrollY) >= document.body.scrollHeight - 150) {
    nav.classList.remove('hidden')
    is_visible_navbar.value = false
  } else if ((prev_scroll.value) > (window.scrollY)) {
    nav.classList.remove('hidden')
    prev_scroll.value = window.scrollY;
    is_visible_navbar.value = false

  } else if ((prev_scroll.value + 50) < window.scrollY) {
    nav.classList.add('hidden')
    prev_scroll.value = window.scrollY;
    is_visible_navbar.value = true
  }
}

onMounted(() => {
  nav = document.getElementById('navbar')
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
      <RouterLink active-class="active" class="link" to="/series">TV</RouterLink>
      <RouterLink active-class="active" class="link" to="/youtube">Youtube</RouterLink>
      <h1>•</h1>
      <RouterLink active-class="active" class="link" to="/anime">Anime</RouterLink>
      <RouterLink active-class="active" class="link" to="/manga">Manga</RouterLink>
      <h1>•</h1>
      <RouterLink active-class="active" class="link" to="/games">Games</RouterLink>
      <h1>•</h1>
      <login-bar></login-bar>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  /*outline: 1px solid red;*/
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 500;

  font-size: 1.2em;

  transition: 250ms;
  transition-delay: 0ms;
  background-color: #36204b;
}

.hidden {
  transform: translate(0, -100%);
  transition-delay: 250ms;
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
  align-items: center;
  max-width: 1000px;
  margin: auto;
  gap: 20px;
  padding: 10px;
  /*outline: 1px solid greenyellow;*/
}

.link {
  /*font-weight: lighter;*/
  font-weight: 300;
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