<script setup>
import {RouterLink} from "vue-router";
</script>

<template>
  <nav>
    <ul>
      <li><RouterLink active-class="active" class="link" to="/">Movies</RouterLink></li>
      <li><RouterLink active-class="active" class="link" to="/manga">Manga</RouterLink></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "NavBar"
}
</script>

<style scoped>
nav {
  position: relative;
  /*width: 100%;*/
  /*display: flex;*/
  justify-content: center;
}
.link, link:visited {
  text-decoration: none;
  color: white;
}
.active {
  font-weight: bold;
}
</style>