<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import Badge from "@/components/media_container/movie_container/sub_components/badge.vue";

let props = defineProps(["media_type"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

let available_badges = ref()

async function get_tags() {
  const url = new URL(`${curr_api}/tag/get`)
  url.searchParams.set('media_type', props['media_type'])

  let result = await fetch(url).then(response => response.json())

  available_badges.value = result.sort((a,b) => a['tier'] > b['tier'])
}
onMounted(()=>{
  get_tags()
})
</script>

<template>
  <div class="badges_wrapper">
    <badge :data="badge" v-for="badge in available_badges" :key="badge.id" :min_size="200"></badge>
  </div>
</template>

<style scoped>
.badges_wrapper {
  display: flex;
  flex-flow: row wrap;
  gap: 5px;
  width: 50%;
  height: 200px;

}
</style>