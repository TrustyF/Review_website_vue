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
const mediaType = ref("game")
</script>

<template>

<!--  <div class="floating_warning dark_accent" id="game_warning">-->
<!--    <h1>⚠️ Spoiler Warning</h1>-->
<!--    <p> Descriptions may contain important story spoilers.<br> Open at your own risk.</p>-->
<!--  </div>-->

  <MediaPageComponent :filters="filters" :rating-desc="ratingDesc" :mediaType="mediaType"></MediaPageComponent>
</template>

<script>

export default {
  name: "GamePage"
}
</script>

<style scoped>
.floating_warning {
  position: fixed;
  /*width: 150px;*/
  right: -100px;
  top: 50px;

  filter: drop-shadow(0 0 4px rgba(231, 22, 22, 1));

  padding: 15px;
  border-radius: 8px;

  align-content: center;

  z-index: 999;
  opacity: 0;
  animation: fadeOut 5s forwards;
  /*animation-delay: 3s;*/
}

@keyframes fadeOut {
  0% {
    opacity: 0;
    right: -100px;
  }
  10% {
    opacity: 1;
    right: 50px;
  }
  90% {
    opacity: 1;
    right: 50px;
  }
  100% {
    opacity: 0;
    right: 50px;

  }

}

.floating_warning h1 {
  font-weight: bold;
  padding-bottom: 10px;
}

.floating_warning p {
  font-size: 0.8em;
}
</style>