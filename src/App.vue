<script setup>
import {inject} from 'vue'
import {RouterView, RouterLink} from 'vue-router'
import NavBar from "@/components/General/NavBar";
import axios from 'axios'
import './styles/globals.css'
import './styles/dark.css'
import CreditsFooter from "@/components/General/CreditsFooter";

const current_api = inject('curr_api')
let mediaRanges = inject('mediaRanges')

function get_media_ranges() {
  axios.get(`${current_api}/media/get_rating_ranges`, {params: {'test': 1, 'good': true}})
      .then(response => {
        if (response.status === 200) {
          mediaRanges.value = response.data
          console.log('get all ranges', mediaRanges)
        }
      })
}

get_media_ranges()

</script>

<template>
  <div class="main">
    <NavBar/>
    <div class="app_wrapper">
      <RouterView/>
    </div>
    <CreditsFooter/>
  </div>
</template>

<style scoped>

.app_wrapper {
  /*outline: 1px solid red;*/
  display: block;
  margin: auto;
  transition: 500ms;
}
</style>