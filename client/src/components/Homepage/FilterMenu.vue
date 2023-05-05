<script setup>
import {defineProps, defineEmits, ref, watch} from 'vue'
import {Collapse} from 'vue-collapsed'
import filterButton from '/public/assets/ui/filter_button.png'

const props = defineProps(['props'])
const emits = defineEmits(['filters'])
let filters = {
  'type': {
    'name': 'Type',
    'available': ["Movie", "Tv-series", "Documentary"],
    'display': ["Movie", "Tv-series", "Documentary"],
    'filter': [],
    'checkbox': true,
  },
  'format': {
    'name': 'Format',
    'available': ["Live-action", "Animated"],
    'display': ["Filmed", "Animated"],
    'filter': [],
    'checkbox': false,
  },
  'region': {
    'name': 'Region',
    'available': ["western", "asian"],
    'display': ["Western", "Asian"],
    'filter': [],
    'checkbox': false,
  },
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
  'length': {
    'name': 'Length',
    'available': ["0", "1", "2", "3"],
    'display': ["-1 hour", "1-2 hours", "2-3 hours", "3+ hours"],
    'filter': [],
    'checkbox': true
  },
  'date_rated': {
    'name': 'Date rated',
    'available': ["0", "1"],
    'display': ["Ascending", "Descending"],
    'filter': [],
  },
  'search_bar': "",
  'extra_settings': {
    'exclude_mode': false
  }
}
const state = ref(false)

let throttle_search = false

const excludeMode = ref(false)

function swap_filter(filter, target, checkbox, button) {

  console.log('swapping filter', filter, target, checkbox, button)

  if (target.includes(filter) === false) {
    if (checkbox === true) {
      target.push(filter)
    } else {
      target[0] = filter
    }
  } else {
    if (checkbox === true) {
      let index = target.indexOf(filter)
      if (index > -1) { // only splice array when item is found
        target.splice(index, 1); // 2nd parameter means remove one item only
      }
    } else {
      target[0] = []
      button.target.checked = false
    }
  }

  emits('filters', filters)
}

function search_bar(event) {
  if (throttle_search === false) {
    throttle_search = true

    setTimeout(function () {
      filters['search_bar'] = event.target.value
      console.log(filters)
      emits('filters', filters)
      throttle_search = false
    }, 300)

  }
}

</script>
<template>
  <div class="filters_nav_wrapper">
    <div class="filter_button_wrapper" @click="state = !state">
      <h1>Filters</h1>
      <img :src="filterButton" alt="filter button" style="width: 15px">
    </div>

    <div class="search_bar_wrapper">
      <label for="search_bar">Search</label>
      <input class="search_bar" type="search" id="search_bar" @input="search_bar">
    </div>

  </div>

  <Collapse :when="state" class="collapse">
    <div class="filter_wrapper">
      <div class="filters">
        <div class="filter_types" v-for="elem in filters" :key="elem['name']">
          <h1 style="text-decoration: underline;padding-bottom: 5px">{{ elem['name'] }}</h1>
          <div v-for="(filter,index) in elem['available']" :key="filter" class="filter_content_list">
            <label class="filter_label">
              <input :type="elem['checkbox'] ? 'checkbox' : 'radio'" :name="elem['name']" style="cursor: pointer"
                     @click="swap_filter(filter,elem['filter'],elem['checkbox'],$event)">
              {{ elem['display'][index] }}
            </label>
          </div>
        </div>
      </div>
    </div>
  </Collapse>

</template>

<style scoped>
.filters_nav_wrapper {
  /*outline: 1px solid red;*/
  display: flex;
  flex-flow: row;
  align-items: center;
  justify-content: center;
  justify-items: center;
  padding: 5px;

  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);
  gap: 20px;
}

.collapse {
  transition: height 300ms ease-in-out;
}

.filter_wrapper {
  padding: 25px 25px 5px 25px;
  /*outline: 2px solid blue;*/
}

.filter_button_wrapper {
  /*outline: 1px solid red;*/
  padding: 12px;
  cursor: pointer;
  user-select: none;
  display: flex;
  flex-flow: row wrap;
  gap: 5px;
}

.filters {
  font-family: Calibri, serif;
  user-select: none;
  font-min-size: 1em;

  height: 250px;
  padding: 20px;

  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  overflow: hidden;

  display: flex;
  justify-content: left;
  align-items: flex-start;
  flex-flow: column wrap;
  align-content: flex-start;
}

.filter_label {
  font-size: 0.9em;
  cursor: pointer;
}

.filter_types {
  min-width: 60px;
  /*outline: 1px solid red;*/
  margin-right: 10px;
}

.search_bar_wrapper {
  /*outline: 1px solid red;*/

  padding: 5px;
  cursor: pointer;
  user-select: none;
  display: flex;
  gap: 5px;
  align-items: center;
}

.search_bar {
  border-radius: 5px;
  border-width: 2px;
  outline: none;
  padding: 2px;
}
</style>