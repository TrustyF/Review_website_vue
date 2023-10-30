<script setup>
import {inject, onMounted, ref} from "vue";
import MediaMaster from "@/components/MediaContainer/MediaMaster.vue";

const curr_api = inject("curr_api");

let movies = ref({})
function test(){

const url = new URL(`${curr_api}/movie/get`)

url.searchParams.set('limit','50')
url.searchParams.set('page','1')
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


  <div class="movie_container_wrapper">
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
.movie_container_wrapper {
  /*outline: 1px solid red;*/
  width: 80%;
  margin: 30px auto 0 auto;
  gap: 10px;

  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
}
</style>