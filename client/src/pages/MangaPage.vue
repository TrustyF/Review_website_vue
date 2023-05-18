<script setup>
import MediaPageComponent from "./MediaPageComponent"
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
    'available': ["5", "4", "3", "2", "1","0"],
    'display': ["5★", "4★", "3★", "2★", "1★","dropped"],
    'filter': [],
    'checkbox': true
  },
  'sort': {
    'name': 'Sort',
    'available': ["0", "1"],
    'display': ["Popular vote", "Date rated"],
    'filter': [null],
  },
  'search_bar': "",
})
let ratingDesc = {
  5: "Masterpiece",
  4: 'Good',
  3: 'Decent',
  2: 'Bad',
  1: 'Terrible',
  0: 'Dropped',
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