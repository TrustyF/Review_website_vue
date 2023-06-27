<script setup>
import {inject} from 'vue'
import {RouterView, RouterLink} from 'vue-router'
import NavBar from "@/components/General/NavBar";
import './styles/globals.css'
import './styles/dark.css'
import CreditsFooter from "@/components/General/CreditsFooter";

let devMode = inject('devMode')

const current_api = inject('curr_api')
let mediaRanges = inject('mediaRanges')

function get_media_ranges() {

  const url = new URL(`${current_api}/media/get_rating_ranges`)
  fetch(url)

      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        }
        return response.json()
      })

      // Process the returned JSON data
      .then(data => {
        mediaRanges.value = data
        if (devMode) console.log('get all ranges', data);
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

get_media_ranges()

</script>

<template>
  <div class="main">
    <NavBar/>
    <div v-if="mediaRanges!=={}" class="app_wrapper">
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