<script setup>
import {RouterLink} from "vue-router";
import logo from '/ui/logo.png'
import {inject, onMounted, ref} from 'vue'
import LoginBar from "@/components/General/LoginBar.vue";
import triple_bars from "/ui/triple_bars.png";
import {clickOutSide as vClickOutSide} from '@mahdikhashan/vue3-click-outside'

const curr_api = inject("curr_api");
let is_mobile = inject("is_mobile")

let edit_mode = inject('edit_mode')
let is_visible_navbar = inject('is_visible_navbar')
let prev_scroll = ref(0)
let nav

let side_menu = ref()
let side_menu_opening = ref(false)

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

function toggle_side_menu() {
  let elem = side_menu.value

  if (side_menu_opening.value) return
  side_menu_opening.value = true

  if (elem.classList.contains('side_hidden')) {
    elem.classList.remove('side_hidden')
  } else {
    elem.classList.add('side_hidden')
  }

  setTimeout(() => {
    side_menu_opening.value = false
  }, 250)
}

function close_side_menu() {
  if (side_menu_opening.value) return

  let elem = side_menu.value
  if (elem.classList.contains('side_hidden')) return;

  elem.classList.add('side_hidden')
}

onMounted(() => {
  nav = document.getElementById('navbar')
  addEventListener('scroll', event => get_scroll_direction())
})
</script>

<template>
  <nav class="dark_accent navbar" id="navbar">
    <div class="nav_wrapper">
      <RouterLink to="/"><img :src="logo" alt="website icon" style="height: 40px"></RouterLink>

      <div v-if="!is_mobile" class="wrapper">
        <RouterLink active-class="active" class="link" to="/">Home</RouterLink>
        <RouterLink active-class="active" class="link" to="/info">Info</RouterLink>
        <h1 class="nav_separator">|</h1>
        <RouterLink active-class="active" class="link" to="/movie">Movies</RouterLink>
        <RouterLink active-class="active" class="link" to="/tv">TV</RouterLink>
        <RouterLink active-class="active" class="link" to="/short">Shorts</RouterLink>
        <RouterLink active-class="active" class="link" to="/youtube">Youtube</RouterLink>
        <h1 class="nav_separator">•</h1>
        <RouterLink active-class="active" class="link" to="/anime">Anime</RouterLink>
        <RouterLink active-class="active" class="link" to="/manga">Manga</RouterLink>
        <RouterLink active-class="active" class="link" to="/comic">Comics</RouterLink>
        <h1 class="nav_separator">•</h1>
        <RouterLink active-class="active" class="link" to="/game">Games</RouterLink>
        <h1 class="nav_separator">•</h1>
        <login-bar></login-bar>
      </div>

      <div v-if="is_mobile" class="wrapper">
        <RouterLink active-class="active" class="link" to="/movie">Movies</RouterLink>
        <RouterLink active-class="active" class="link" to="/tv">TV</RouterLink>
        <RouterLink active-class="active" class="link" to="/manga">Manga</RouterLink>
      </div>

      <div v-if="is_mobile" @click="toggle_side_menu" class="mobile_wrapper">
        <img alt="menu" :src="triple_bars" class="triple_bars">
      </div>

    </div>
  </nav>

  <div class="side_menu side_hidden"
       ref="side_menu" v-click-out-side="close_side_menu">
    <div class="side_home">
    <RouterLink active-class="active" @click="toggle_side_menu" class="link_side" to="/">Home</RouterLink>
    <RouterLink active-class="active" @click="toggle_side_menu" class="link_side" to="/info">Info</RouterLink>
    </div>
    <div style="height: 20px"></div>
    <RouterLink active-class="active" @click="toggle_side_menu" class="link_side" to="/movie">Movies</RouterLink>
    <RouterLink active-class="active" @click="toggle_side_menu" class="link_side" to="/tv">TV</RouterLink>
    <RouterLink active-class="active" @click="toggle_side_menu" class="link_side" to="/short">Shorts</RouterLink>
    <RouterLink active-class="active" @click="toggle_side_menu" class="link_side" to="/youtube">Youtube</RouterLink>
    <div class="horiz_separator"></div>
    <RouterLink active-class="active" @click="toggle_side_menu" class="link_side" to="/anime">Anime</RouterLink>
    <RouterLink active-class="active" @click="toggle_side_menu" class="link_side" to="/manga">Manga</RouterLink>
    <RouterLink active-class="active" @click="toggle_side_menu" class="link_side" to="/comic">Comics</RouterLink>
    <div class="horiz_separator"></div>
    <RouterLink active-class="active" @click="toggle_side_menu" class="link_side" to="/game">Games</RouterLink>
  </div>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 500;

  overflow-x: scroll;

  font-size: 1.2em;

  transition: 250ms;
  transition-delay: 0ms;
  background-color: #36204b;
  /*background: linear-gradient(to top, #6d4594 0%, #36204b 100%);*/
}

.nav_wrapper {
  display: flex;
  flex-flow: row;
  align-items: flex-start;
  max-width: 1080px;
  margin: auto;
  gap: 20px;
  padding: 10px;
}

.hidden {
  transform: translate(0, -100%);
  transition-delay: 250ms;
}

.triple_bars {
  height: 30px;
  filter: invert();
  cursor: pointer;
}

.side_menu {
  position: fixed;
  /*gap: 20px;*/
  padding: 20px;
  left: 0;
  top: 0;
  bottom: 0;
  display: flex;
  flex-flow: column;
  z-index: 500;
  background-color: #36204b;
  filter: drop-shadow(2px 0 10px black);
  transition: 250ms;
}

.side_hidden {
  transform: translate(-100%, 0);
  filter: unset;
}

.link_side {
  width: 200px;
  font-weight: 300;
  font-size: 1.2em;
  /*background-color: #4b2d67;*/
  padding: 20px 20px 20px 0;
}
.side_home {
  background-color: #26113a;
  padding: 20px 40px 20px 20px;
  margin: -20px -20px -10px -20px;
}

.link_side, .link_side:visited {
  text-decoration: none;
  color: white;
}

.horiz_separator {
  margin: 10px 0 10px 0;
  height: 1px;
  background-color: white;
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
  padding: 10px 0 10px 0;
  /*outline: 1px solid red;*/
  height: 20px;
  /*gap: 20px;*/
}

.mobile_wrapper {
  position: absolute;
  /*display: flex;*/
  /*flex-flow: row;*/
  top: 0;
  right: 0;
  padding: 15px;
  cursor: pointer;
}
.nav_separator {
  padding: 10px;
}
.link {
  /*font-weight: lighter;*/
  font-weight: 300;
  /*outline: 1px solid red;*/
  padding: 25px 10px 25px 10px;
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