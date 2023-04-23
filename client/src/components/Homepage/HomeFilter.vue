<script setup>
import {defineProps,defineEmits} from 'vue'
const props = defineProps(['props'])
const emits = defineEmits(['filters'])
const filters ={
  'type': {
    'name': 'Type',
    'available': ["Movie", "Tv-series", "Documentary"],
    'filter': [],
  },
  'format': {
    'name': 'Format',
    'available': ["Live-action", "Animated"],
    'filter': [],
  },
  'genre': {
    'name': 'Genre',
    'available': ["Action", "Adventure", "Crime", "Comedy", "Drama", "Family", "Horror", "Mystery", "Science Fiction", "Thriller"],
    'filter': [],
  },
  'rating': {
    'name': 'Rating',
    'available': ["9", "8", "7", "6", "5", "4", "3", "2", "1"],
    'filter': [],
  },
  'length': {
    'name': 'Length',
    'available': ["1", "2", "3"],
    'filter': [],
  },
}

function swap_filter(filter, target) {
  console.log('swapping filter')
  if (target.includes(filter) === false) {
    target.push(filter)
  }
  else
  {
    let index = target.indexOf(filter)
    if (index > -1) { // only splice array when item is found
      target.splice(index, 1); // 2nd parameter means remove one item only
    }
  }
  emits('filters',filters)
}

</script>
<template>
  <div class="filters">
    <h1 style="font-weight: bold; font-size: 1.5em">Filters</h1>
    <label class="filter_label">
      <input type="checkbox" style="cursor: pointer" @click="excludeMode = !excludeMode">
      Invert
    </label>

    <div class="filter_types" v-for="elem in filters" :key="elem['name']">
      <h1 style="text-decoration: underline;padding-bottom: 5px">{{ elem['name'] }}</h1>
      <div v-for="filter in elem['available']" :key="filter" class="filter_content_list">
        <label class="filter_label">
          <input type="checkbox" style="cursor: pointer" @change="swap_filter(filter,elem['filter'])">
          {{ filter }}
        </label>
      </div>
    </div>
  </div>
</template>

<style scoped>
.filters {
  font-family: Calibri, serif;
  user-select: none;
  position: fixed;
  width: 150px;
  font-min-size: 1em;
  /*height: 200px;*/

  padding: 20px;
  margin: 15px 0 0 25px;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);

  display: flex;
  flex-flow: column;
  /*grid-template-areas:"left right";*/
  gap: 8px;
}

.filter_content_list {
  /*outline: red 1px solid;*/
  width: 100%;
}

.filter_label {
  font-size: 0.9em;
  cursor: pointer;
}
</style>