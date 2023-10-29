<script setup>
import {inject, onMounted, ref} from "vue";
import MediaMaster from "@/components/MediaContainer/MediaMaster.vue";

const curr_api = inject("curr_api");

let movie = ref({})
function test(){

const url = new URL(`${curr_api}/movie/get`)

url.searchParams.set('limit','5')
url.searchParams.set('page','0')
url.searchParams.set('order','name')

fetch(url)
  .then(response => response.json())
  .then(data => {
    console.log(data);
    movie.value = data[0]
  })

}

onMounted(()=>{
  test()
})

</script>

<template>
  <div>
    <MediaMaster :data="movie"></MediaMaster>
  </div>
</template>

<style scoped>
</style>