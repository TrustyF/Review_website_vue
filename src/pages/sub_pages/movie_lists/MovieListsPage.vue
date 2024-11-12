<script setup>
import TierFeed from "../../../components/Tierlists/TierFeed.vue";

import skeleton_vulvine_img from "/tier_list_images/skeleton_vulvina.jpg"
import best_worst from "/tier_list_images/BOTW.jpg"

let tier_lists = [
  {
    'name': 'Best of the worst',
    'desc': 'The most entertaining pieces of garbage',
    'image': best_worst,
    'link': '/movie_lists/best_of_the_worst'
  },
  {
    'name': 'Short films',
    'desc': 'Shorts from across the globe',
    'image': skeleton_vulvine_img,
    'link': '/movie_lists/shorts'
  },
]


</script>

<template>
  <tier-feed :box_size="[700,500]" :box_scale="0.4" :data="tier_lists" :row_num="3"></tier-feed>
</template>