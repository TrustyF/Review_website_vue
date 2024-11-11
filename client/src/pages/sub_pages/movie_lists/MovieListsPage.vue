<script setup>
import TierFeed from "../../../components/Tierlists/TierFeed.vue";

import skeleton_vulvine_img from "/tier_list_images/skeleton_vulvina.jpg"

let tier_lists = [
  {
    'name': 'Short films',
    'desc': '',
    'image': skeleton_vulvine_img,
    'link': '/movie_lists/shorts'
  },
  {
    'name': 'Best of the worst',
    'desc': 'All the most entertaining pieces of garbage',
    'image': skeleton_vulvine_img,
    'link': '/movie_lists/best_of_the_worst'
  }
]


</script>

<template>
  <tier-feed :box_size="[700,500]" :box_scale="0.4" :data="tier_lists" :row_num="3"></tier-feed>
</template>