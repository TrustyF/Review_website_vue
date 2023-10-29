<script setup>
import {inject, onMounted, ref} from "vue";
import MediaMaster from "@/components/MediaContainer/MediaMaster.vue";

const curr_api = inject("curr_api");

let movies = ref({})
function test(){

const url = new URL(`${curr_api}/movie/get`)

url.searchParams.set('limit','5')
url.searchParams.set('page','0')
url.searchParams.set('order','name')

fetch(url)
  .then(response => response.json())
  .then(data => {
    console.log(data);
    movies.value = data
  })

}

onMounted(()=>{
  test()
})

</script>

<template>
  <div class="test">
    <div v-for="mov in movies" :key="mov['id']">
      <MediaMaster :data="mov"></MediaMaster>
    </div>
  </div>
</template>

<style scoped>
.test {
  width: 100%;
  display: flex;
  flex-flow: row wrap;
  gap: 10px;
}
</style>