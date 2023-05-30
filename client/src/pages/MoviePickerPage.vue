<script setup>
import {ref, onMounted, onUnmounted, inject} from 'vue'
import RandomGenreBanner from '@/components/Media/banners/RandomGenreBanner'

let darkMode = inject('darkMode')

</script>

<template>

  <RandomGenreBanner mediaType="movie"></RandomGenreBanner>
</template>

<script>

</script>

<style scoped>

</style>