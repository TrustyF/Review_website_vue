<script setup>
import {defineProps, defineEmits, ref, watch} from 'vue'

const props = defineProps(['rating'])

function getRankDetails(rank) {
  if (rank === 10) return 'Perfect'
  if (rank === 9) return 'Near perfect masterpiece'
  if (rank === 8) return 'Extremely good'
  if (rank === 7) return 'Quite good'
  if (rank === 6) return 'Good with flaws'
  if (rank === 5) return "Meh"
  if (rank === 4) return 'Bad'
  if (rank === 3) return 'Fucking bad'
  if (rank === 2) return 'Holy shit bad'
  if (rank === 1) return 'Affront to god'
}
</script>

<template>
  <div class="rating_container">
    <div class="rating_content">
      <h1 class="rating_title">{{ rating + "★" }}</h1>
      <h1 class="rating_desc"> {{ getRankDetails(rating) }}</h1>
    </div>
  </div>
</template>

<script>
export default {
  name: "RatingHeader"
}
</script>
<style scoped>
.rating_container {
  width: 100%;
  user-select: none;
  position: sticky;
  top: 20px;
  margin-bottom: 10px;
  /*outline: 1px red solid;*/
}

.rating_content {
  background-color: white;
  /*outline: 1px blue solid;*/

  width: fit-content;

  display: flex;
  justify-content: flex-start;
  align-items: center;
  flex-flow: row wrap;
  align-content: flex-start;

  gap: 15px;

  padding: 10px 10px 10px 10px;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}

.rating_title {
  font-family: "Arial Black", serif;
  font-size: 2em;
}

.rating_desc {
  font-family: Calibri, serif;
  font-size: 1em;
}
</style>