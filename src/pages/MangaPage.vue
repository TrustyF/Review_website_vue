<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MovieContainer from "@/components_V2/media_container/movie_container/MovieContainer.vue";
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
              :media_type="'manga'"
              :media_container="MovieContainer"
              :media_size="[256,360]"
              :media_scale="0.7"
  ></media-feed>
  <media-feed-mobile v-else
                     :media_type="'manga'"
                     :media_container="MovieContainerMobile"
                     :media_size="[256,360]"
                     :media_scale="0.2"
  ></media-feed-mobile>
</template>
