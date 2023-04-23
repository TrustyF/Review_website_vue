<script setup>
import {defineProps, defineEmits, ref, watch} from 'vue'
import {Collapse} from 'vue-collapsed'
import filterButton from '/public/assets/ui/filter_button.png'

const props = defineProps(['props'])
const emits = defineEmits(['filters'])
const filters = {
  'type': {
    'name': 'Type',
    'available': ["Movie", "Tv-series", "Documentary"],
    'display': ["Movie", "Tv-series", "Documentary"],
    'filter': [],
  },
  'format': {
    'name': 'Format',
    'available': ["Live-action", "Animated"],
    'display': ["Filmed", "Animated"],
    'filter': [],
  },
  'genre': {
    'name': 'Genre',
    'available': ["Action", "Adventure", "Crime", "Comedy", "Drama", "Family", "Horror", "Mystery", "Science Fiction", "Thriller"],
    'display': ["Action", "Adventure", "Crime", "Comedy", "Drama", "Family", "Horror", "Mystery", "Science Fiction", "Thriller"],
    'filter': [],
  },
  'rating': {
    'name': 'Rating',
    'available': ["9", "8", "7", "6", "5", "4", "3", "2", "1"],
    'display': ["9★", "8★", "7★", "6★", "5★", "4★", "3★", "2★", "1★"],
    'filter': [],
  },
  'length': {
    'name': 'Length',
    'available': ["0", "1", "2", "3"],
    'display': ["-1 hour", "1-2 hours", "2-3 hours", "3+ hours"],
    'filter': [],
  },
  'date_rated': {
    'name': 'Date rated',
    'available': ["0", "1"],
    'display': ["Ascending", "Descending"],
    'filter': [],
  },
  'extra_settings': {
    'exclude_mode': false
  }
}
const state = ref(false)

const excludeMode = ref(false)

function swap_filter(filter, target) {
  console.log('swapping filter')
  if (target.includes(filter) === false) {
    target.push(filter)
  } else {
    let index = target.indexOf(filter)
    if (index > -1) { // only splice array when item is found
      target.splice(index, 1); // 2nd parameter means remove one item only
    }
  }
  emits('filters', filters)
}

</script>
<template>

  <div class="filter_button" @click="state = !state">
    <div class="button_padding"></div>
    <img :src="filterButton" alt="filter button" style="width: 15px;margin-right: 5px">
    <h1>Filters</h1>
  </div>

  <Collapse :when="state" class="collapse">
    <div class="filter_wrapper">
      <div class="filters">
        <div class="filter_types" v-for="elem in filters" :key="elem['name']">
          <h1 style="text-decoration: underline;padding-bottom: 5px">{{ elem['name'] }}</h1>
          <div v-for="(filter,index) in elem['available']" :key="filter" class="filter_content_list">
            <label class="filter_label">
              <input type="checkbox" style="cursor: pointer" @change="swap_filter(filter,elem['filter'])">
              {{ elem['display'][index] }}
            </label>
          </div>
        </div>
      </div>
    </div>
  </Collapse>

</template>

<style scoped>
.collapse {
  transition: height 300ms ease-in-out;
}

.button_padding {
  /*outline: 1px red solid;*/
  position: absolute;
  width: 90px;
  height: 45px;
  margin: 10px;
  transform: translate(-20px, -25px);
}

.filter_wrapper {
  padding: 25px 25px 5px 25px;
}

.filter_button {
  cursor: pointer;
  user-select: none;
  margin: 20px 25px 0 25px;
  display: flex;
  flex-flow: row wrap;
}

.filters {
  font-family: Calibri, serif;
  user-select: none;
  font-min-size: 1em;

  height: 220px;
  padding: 20px;

  /*margin: 25px 25px 0 25px;*/
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  overflow: hidden;

  display: flex;
  justify-content: left;
  align-items: flex-start;
  flex-flow: column wrap;
  align-content: flex-start;

  gap: 10px;
}

.filter_label {
  font-size: 0.9em;
  cursor: pointer;
}
</style>