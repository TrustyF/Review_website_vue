<script setup>
import {RouterLink} from "vue-router";
import logo from '@/assets/ui/logo.png'
import {inject, onMounted, ref} from 'vue'

let editMode = inject('editMode')
let prev_scroll = ref(0)
let nav

function get_scroll_direction(event) {

  if (window.scrollY === 0){
    nav.classList.remove('hidden')
  }
  else if ((prev_scroll.value - 400) > (window.scrollY)) {
    nav.classList.remove('hidden')
    prev_scroll.value = window.scrollY;

  } else if ((prev_scroll.value) < window.scrollY) {
    nav.classList.add('hidden')
    prev_scroll.value = window.scrollY;
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
<!--      <RouterLink active-class="active" class="link" to="/">Home</RouterLink>-->
<!--      <h1>|</h1>-->
      <RouterLink active-class="active" class="link" to="/movies">Movies</RouterLink>
      <RouterLink active-class="active" class="link" to="/series">Series</RouterLink>
      <RouterLink active-class="active" class="link" to="/shorts">Shorts</RouterLink>
      <h1>•</h1>
      <RouterLink active-class="active" class="link" to="/anime">Anime</RouterLink>
      <RouterLink active-class="active" class="link" to="/manga">Manga</RouterLink>
      <h1>•</h1>
      <RouterLink active-class="active" class="link" to="/games">Games</RouterLink>
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
  z-index: 50;

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


.wrapper {
  display: flex;
  flex-flow: row wrap;
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