<script setup>
import MediaPageComponent from "./components/MediaPageComponent"
import {ref, onMounted} from 'vue'

let filters = ref({
  'genre': {
    'name': 'Genre',
    'available': ["Action", "Adventure", "Crime", "Comedy", "Drama", "Family", "Horror", "Mystery", "Romance", "Science Fiction", "Thriller"],
    'display': ["Action", "Adventure", "Crime", "Comedy", "Drama", "Family", "Horror", "Mystery", "Romance", "Science Fiction", "Thriller"],
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
  'content': {
    'name': 'Content',
    'available': ["safe", "suggestive", "erotica", "pornographic"],
    'display': ["Safe", "Suggestive", "Erotic", "Pornographic"],
    'filter': ["safe", "suggestive"],
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
const mediaType = "manga"
</script>

<template>
  <MediaPageComponent :filters="filters" :rating-desc="ratingDesc" :mediaType="mediaType"></MediaPageComponent>
</template>

<script>

export default {
  name: "MangaPage"
}
</script>