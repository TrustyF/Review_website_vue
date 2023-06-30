<script setup>
import MediaPageComponent from "./components/MediaPageComponent"
import {ref, onMounted} from 'vue'

let filters = ref({
  'format': {
    'name': 'Format',
    'available': ["Live-action", "Animated"],
    'display': ["Filmed", "Animated"],
    'filter': [],
    'checkbox': false,
  },
  'genre': {
    'name': 'Genre',
    'available': ["Action & Adventure", "Crime", "Comedy", "Drama", "Mystery", "Sci-Fi & Fantasy"],
    'display': ["Action & Adventure", "Crime", "Comedy", "Drama", "Mystery", "Sci-Fi & Fantasy"],
    'filter': [],
    'checkbox': true
  },
  'rating': {
    'name': 'Rating',
    'available': ["9", "8", "7", "6", "5", "4", "3", "2", "1"],
    'display': ["9★", "8★", "7★", "6★", "5★", "4★", "3★", "2★", "1★"],
    'filter': [],
    'checkbox': true
  },
  'length': {
    'name': 'Length',
    'available': ["1_hour", "1_2_hour", "2_3_hour", "3_hour"],
    'display': ["< 1 hour", "1-2 hours", "2-3 hours", "3+ hours"],
    'filter': [],
    'checkbox': true
  },
  'sort': {
    'name': 'Sort',
    'available': ["popular_vote", "release_date"],
    'display': ["Popular vote", "Release date"],
    'filter': [null],
  },
  'search_bar': "",
})
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
  <MediaPageComponent :filters="filters" :rating-desc="ratingDesc" :mediaType="mediaType"></MediaPageComponent>
</template>