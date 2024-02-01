<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import TierFeed from "@/components/Tierlists/TierFeed.vue";

import riot_games_img from "/tier_list_images/riot_games.jpg"
import youtube_short_films_img from "/tier_list_images/youtube_short_films.jpg"
import youtube_animations_img from "/tier_list_images/youtube_animations.jpg"
import youtube_shows_img from "/tier_list_images/youtube_shows.jpg"

let tier_lists = [
  {
    'name': 'Riot games media',
    'image': riot_games_img,
    'link':'/youtube/riot_games_media'
  },
  {
    'name': 'Youtube short films',
    'image': youtube_short_films_img,
    'link':'/youtube/yt_short_films'
  },
  {
    'name': 'Youtube animations',
    'image': youtube_animations_img,
    'link':'/youtube/yt_animations'
  },
  {
    'name': 'Youtube shows',
    'image': youtube_shows_img,
    'link':'/youtube/yt_shows'
  },
  {
    'name': 'Youtube',
    'image': undefined,
    'link':'/youtube/youtube_debug'
  },
]

onMounted(() => {
  window.scroll(0, 0)
})
</script>

<template>
  <tier-feed :box_size="[700,500]" :box_scale="0.5" :data="tier_lists"></tier-feed>
</template>