<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaMaster from "../Master/Base/MediaMaster.vue";
import MediaCollapsed from "@/components/MediaContainer/Master/Collapsed/MediaCollapsed.vue";
import blue_star from '@/assets/ui/blue_star.png'

let props = defineProps(["media_type"]);
const curr_api = inject("curr_api");

let media = ref([])
let media_grouped = ref([])

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

        data.forEach(entry => {
          media.value.push(entry)
        })

        media_grouped.value = media.value.reduce((r, e, index) => {
          if (!r[e['user_rating']]) r[e['user_rating']] = [e]
          else r[e['user_rating']].push(e)
          return r;
        }, {})

        console.log(media_grouped.value)


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
  // console.log(document.body.clientWidth)
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

  <div v-if="!is_mobile" id="media_container">
    <div class="rating_box"  v-for="rating in Object.keys(media_grouped).reverse()" :key="rating">

      <div class="rating_separator">
        <h1 style="height: 0.8em;font-weight: 500;font-size: 1.5em"> {{ rating }} </h1>
        <img :src="blue_star" alt="blue_star" style="width: 20px">
      </div>

      <div class="media_container_wrapper">
        <div v-for="med in media_grouped[rating]" :key="med['id']">
          <MediaMaster :data="med"></MediaMaster>
        </div>
      </div>

    </div>
  </div>

  <div v-else id="media_container">
    <div class="rating_box"  v-for="rating in Object.keys(media_grouped).reverse()" :key="rating">

      <div class="rating_separator_mobile">
        <h1 style="height: 0.8em;font-weight: 500;font-size: 1em"> {{ rating }} </h1>
        <img :src="blue_star" alt="blue_star" style="width: 10px">
      </div>

      <div class="media_container_wrapper_mobile">
        <div v-for="med in media_grouped[rating]" :key="med['id']">
                <media-collapsed :data="med"></media-collapsed>
        </div>
      </div>

    </div>
  </div>

<!--  <div class="media_container_wrapper_mobile" id="media_container" v-else>-->
<!--    <div v-for="med in media" :key="med['id']">-->
<!--      <media-collapsed :data="med"></media-collapsed>-->
<!--    </div>-->
<!--  </div>-->

</template>

<style scoped>

.media_container_wrapper {
  gap: 20px;
  justify-items: center;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
}
.rating_box {
  position: relative;
}

.rating_separator {
  /*outline: 1px solid red;*/
  width: fit-content;
  padding: 10px;
  margin: 15px 0 15px 0;
  background-color: #2d2d41;
  border-radius: 8px;
  position: sticky;
  top: 10px;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 5px;
}
.rating_separator_mobile {
  /*outline: 1px solid red;*/
  width: fit-content;
  padding: 7px;
  margin: 5px 0 5px 0;
  background-color: #2d2d41;
  border-radius: 8px;
  position: sticky;
  top: 10px;
  z-index: 5;
  display: flex;
  align-items: center;
  gap: 3px;
}
.media_container_wrapper_mobile {
  gap: 10px;
  justify-items: center;
  display: flex;
  flex-flow: column nowrap;
}
</style>