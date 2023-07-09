<script setup>
import {ref, onMounted, onUnmounted, inject} from 'vue'
import RandomGenreBanner from '@/components/Media/banners/RandomGenreBanner'
import FilterMenu from "@/components/Media/general/FilterMenu";
import {eventThrottle} from "@/utils";

let num_media_fit = ref(0)
let banners_media = ref([[],[],[],[],[]])

let devMode = inject('devMode')
let sessionSeed = inject('sessionSeed')
let mediaRanges = inject('mediaRanges')
const current_api = inject('curr_api')

let bannerLoaded = false

function get_home_banners() {
  console.log('getting home banners')

  const url = new URL(`${current_api}/media/get_home_banners`)
  const params = {
    'media_type': 'movie',
    'max_media': num_media_fit.value * 5,
    'session_seed': sessionSeed
  }

  fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(params)
  })

      // Handle http error
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`)
        }
        return response.json()
      })

      // Process the returned JSON data
      .then(data => {
        banners_media.value = data
        bannerLoaded = true
        console.log('banner loaded')
        // if (devMode) console.log('recent release banner', data);
      })

      // Handle any errors that occurred during the fetch
      .catch(error => {
        console.error('Error:', error);
      });
}

function calc_screen_fit() {

  let w_box = document.getElementById("genre_box").getBoundingClientRect()
  // let w_box = document.getElementById("main_banner").getElementById("genre_box").getBoundingClientRect()
  let gap = 20
  let media_width = 200
  let fit_num = Math.floor(w_box.width / (media_width + (gap)))

  if (num_media_fit.value !== fit_num) {
    num_media_fit.value = fit_num
    console.log(num_media_fit.value)
    get_home_banners()
  }

}

onMounted(() => {
  calc_screen_fit()
  addEventListener('resize', eventThrottle(calc_screen_fit, 100))
})
onUnmounted(() => {
  removeEventListener('resize', calc_screen_fit)
})

</script>

<template>
  <div class="pick_page_feed_wrapper">
<!--    <div v-if="bannerLoaded">-->
      <div>
        <h1 class="headers"> What are you in the mood for ?</h1>
        <RandomGenreBanner mediaType="movie"
                           :banner-media="banners_media"
                           :banner-index="0"
                           :bannerFit="num_media_fit"
        ></RandomGenreBanner>
      </div>
      <div>
        <h1 class="headers">How about a recent release.</h1>
        <RandomGenreBanner mediaType="movie"
                           :banner-media="banners_media"
                           :banner-index="1"
                           :bannerFit="num_media_fit"
        ></RandomGenreBanner>
      </div>
      <div>
        <h1 class="headers">What I watched recently.</h1>
        <RandomGenreBanner mediaType="movie"
                           :banner-media="banners_media"
                           :banner-index="2"
                           :bannerFit="num_media_fit"
        ></RandomGenreBanner>
      </div>
      <div>
        <h1 class="headers">Longer form content perhaps ?</h1>
        <RandomGenreBanner mediaType="tv"
                           :banner-media="banners_media"
                           :banner-index="3"
                           :bannerFit="num_media_fit"
        ></RandomGenreBanner>
      </div>
      <div>
        <h1 class="headers">Looking for a good read ?</h1>
        <RandomGenreBanner mediaType="manga"
                           :banner-media="banners_media"
                           :banner-index="4"
                           :bannerFit="num_media_fit"
        ></RandomGenreBanner>
      </div>
<!--    </div>-->
  </div>
</template>

<script>

</script>

<style scoped>
.pick_page_feed_wrapper {
  outline: 1px solid green;
  padding: 30px 0 30px 0;
  /*width: 80%;*/
  margin: auto;
  display: flex;
  flex-flow: column;
  gap: 50px;
}

.headers {
  font-weight: bold;
  font-size: 1.2em;
  margin: 0 0 20px 10%;
}
</style>