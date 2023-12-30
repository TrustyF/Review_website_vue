<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import YoutubeContainer from "@/components_V2/media_container/youtube_container/YoutubeContainer.vue";
import MovieContainerMobile from "@/components_V2/media_container/movie_container/MovieContainerMobile.vue";
import MediaFeed from "@/components_V2/media_feed/MediaFeed.vue";
import MediaFeedMobile from "@/components_V2/media_feed/MediaFeedMobile.vue";

let is_mobile = ref(false)

function check_mobile() {
  is_mobile.value = document.body.clientWidth < 500;
}

onMounted(() => {
  check_mobile()
  addEventListener("resize", () => check_mobile())
})
</script>

<template>
  <media-feed v-if="!is_mobile"
              :media_type="'short'"
              :media_container="YoutubeContainer"
              :media_size="[320,180]"
              :media_scale="1"
  ></media-feed>
  <media-feed-mobile v-else
                     :media_type="'short'"
                     :media_container="MovieContainerMobile"
                     :media_size="[320,180]"
                     :media_scale="1"
  ></media-feed-mobile>
</template>
