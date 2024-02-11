<script setup>
import {ref, onMounted, inject, provide} from 'vue'
import TierFeed from "../components/Tierlists/TierFeed.vue";

import riot_games_img from "/tier_list_images/riot_games.jpg"
import fever_ghost_img from "/tier_list_images/fever_the_ghost.jpg"
import dont_thug_img from "/tier_list_images/dont_thug_me.jpg"
import hazbin_img from "/tier_list_images/hazbin_hotel.jpg"
import skeleton_vulvine_img from "/tier_list_images/skeleton_vulvina.jpg"
import lemmino_plane_img from "/tier_list_images/lemmino_plane.jpg"
import sombra_img from "/tier_list_images/sombra_img.jpg"
import hbomber_img from "/tier_list_images/hbomber_img.jpg"

let tier_lists = [
  {
    'name': 'Riot games media',
    'image': riot_games_img,
    'link':'/youtube/riot_games_media'
  },
  {
    'name': 'Short films',
    'image': skeleton_vulvine_img,
    'link':'/youtube/yt_short_films'
  },
  {
    'name': 'Animations',
    'image': dont_thug_img,
    'link':'/youtube/yt_animations'
  },
  {
    'name': 'Music videos',
    'image': fever_ghost_img,
    'link':'/youtube/yt_music_videos'
  },
  {
    'name': 'Overwatch media',
    'image': sombra_img,
    'link':'/youtube/yt_overwatch_cinematics'
  },
  {
    'name': 'Comedy',
    'image': sombra_img,
    'link':'/youtube/yt_comedy'
  },
  {
    'name': 'Documentaries',
    'image': lemmino_plane_img,
    'link':'/youtube/yt_documentaries'
  },
  {
    'name': 'Video essays',
    'image': hbomber_img,
    'link':'/youtube/yt_essays'
  },
  {
    'name': 'Shows',
    'image': hazbin_img,
    'link':'/youtube/yt_shows'
  },
]

onMounted(() => {
  window.scroll(0, 0)
})
</script>

<template>
  <tier-feed :box_size="[700,500]" :box_scale="0.4" :data="tier_lists" :row_num="3"></tier-feed>
</template>