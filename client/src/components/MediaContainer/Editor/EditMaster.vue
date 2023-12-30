<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaExpanded from "@/components/MediaContainer/Expanded/Base/MediaExpanded.vue";
import MediaMaster from "@/components/MediaContainer/Master/Base/MediaMaster.vue";

let props = defineProps(["test"]);
const curr_api = inject("curr_api");
const edit_media = inject("edit_media");

const extra_posters = ref([])

async function get_extra_posters() {
  const url = new URL(`${curr_api}/media/get_extra_posters`)
  url.searchParams.set('id', edit_media['id'])
  url.searchParams.set('type', edit_media['type'])

  let result = await fetch(url).then(response => response.json())
  console.log(result)
  extra_posters.value = result
}

onMounted(() => {
  get_extra_posters()
})
</script>

<template>

  <div class="edit_master_wrapper">
    <div class="poster_pane">
      <div class="preview">
        <media-master :data="edit_media"></media-master>
      </div>
      <div class="extra_posters">
        <div class="extra_poster" v-for="poster in extra_posters" :key="poster['id']">
          <img :src="poster" alt="extra_poster">
        </div>
      </div>
    </div>

    <div class="details_pane">
      <div v-for="(val,key) in edit_media" :key="key" style="display: flex;flex-flow: column wrap">
        <label :for="key">{{ key }}</label>
        <input :id="key" :type="typeof val" :value="val"
               @change="edit_media[key] = $event.target._value">
      </div>
    </div>
  </div>

</template>

<style scoped>
.edit_master_wrapper {
  background-color: #131215;
  position: relative;
  z-index: 50;
  display: flex;
  flex-flow: column nowrap;
}

.poster_pane {
  outline: 1px solid red;
}

.details_pane {
  outline: 1px solid red;
  display: flex;
  flex-flow: row wrap;
  gap: 5px;
  /*width: 600px;*/
}
</style>