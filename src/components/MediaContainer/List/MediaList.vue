<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaMaster from "../Master/Base/MediaMaster.vue";
import MediaCollapsed from "@/components/MediaContainer/Master/Collapsed/MediaCollapsed.vue";

let props = defineProps(["media_type"]);
const curr_api = inject("curr_api");

let media = ref([])

let media_limit = ref(30)
let media_page = ref(0)
let media_order = ref('rating')

let is_loading_more_media = ref(false)
let is_all_media_loaded = ref(false)
let is_mobile = ref(false)

function get_media() {

  const url = new URL(`${curr_api}/media/get`)
  console.log(`${curr_api}/media/get`)

  url.searchParams.set('limit', String(media_limit.value))
  url.searchParams.set('page', String(media_page.value))
  url.searchParams.set('order', media_order.value)
  console.log(props['media_type'])
  url.searchParams.set('type', props['media_type'])

  fetch(url)
      .then(response => response.json())
      .then(data => {

        if (data.length < 1) {
          return
        }

        data.forEach(entry =>{
          media.value.push(entry)
        })
        console.log(media.value)
        is_loading_more_media.value = false
        scroll_media_loader()
      })

}

function scroll_media_loader() {
  let rect = document.getElementById('media_container').getBoundingClientRect()

  if (rect.bottom <= (window.innerHeight + (window.innerHeight / 2)) &&
      !is_loading_more_media.value &&
      !is_all_media_loaded.value) {

    console.log('loading more media')
    is_loading_more_media.value = true
    media_page.value += 1
    get_media()
  }
}

function check_mobile() {
  console.log(document.body.clientWidth)
  is_mobile.value = document.body.clientWidth < 500;
}

onMounted(() => {
  get_media()
  check_mobile()
  addEventListener("scroll", () => scroll_media_loader())
  addEventListener("resize", () => check_mobile())
})

</script>

<template>

  <div class="media_container_wrapper" id="media_container" v-if="!is_mobile">
    <div v-for="med in media" :key="med['id']">
      <MediaMaster :data="med"></MediaMaster>
    </div>
  </div>

  <div class="media_container_wrapper_mobile" id="media_container" v-else>
    <div class="list_box_element" v-for="med in media" :key="med['id']">
      <media-collapsed :data="med"></media-collapsed>
    </div>
  </div>

</template>

<style scoped>

.media_container_wrapper {
  outline: 1px solid red;
  /*width: 80%;*/
  margin: 90px 30px 0 30px;
  gap: 20px;
  justify-items: center;
  /*align-items: center;*/

  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
}

.media_container_wrapper_mobile {
  outline: 1px solid greenyellow;
  margin: 90px 10px 0 10px;
  gap: 10px;
  justify-items: center;
  display: flex;
  flex-flow: column nowrap;
}
</style>