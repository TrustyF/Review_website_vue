<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import MediaFeed from "../components/media_feed/MediaFeed.vue";
import MediaBanner from "../components/MediaBanner/MediaBanner.vue";

</script>

<template>
  <div class="banner" style="padding-top: 100px">
    <media-banner :ratings=[0,10]
                  :order="'date_added'"
                  :media_types="[]"
                  :size_override="[528, 704]"></media-banner>
  </div>
  <media-feed :media_types="['all']"
              :tier_lists="['all']"
              :media_container_type="'movie'"
              :media_container_type_override="'movie'"
  ></media-feed>
</template>