<script setup>
import MediaPageComponent from "@/pages/components/MediaPageComponent.vue"
import {ref, onMounted} from 'vue'

let ratingDesc = {
  9: 'Near perfect masterpiece',
  8: 'Extremely good',
  7: 'Very good',
  6: 'Good with flaws',
  5: "Meh",
  4: 'Bad',
  3: 'Fucking bad',
  2: 'Holy shit bad',
  1: 'Affront to god',
}
const mediaType = ref("anime")
</script>

<template>
  <MediaPageComponent :rating-desc="ratingDesc" :mediaType="mediaType"></MediaPageComponent>
</template>