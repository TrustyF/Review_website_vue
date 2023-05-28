<script setup>
import {defineProps, defineEmits, ref, watchEffect, onMounted, watch, toRefs, inject} from 'vue'
import {Collapse} from 'vue-collapsed'
import filterButton from '/public/assets/ui/filter_button.png'
import crossButton from '/public/assets/ui/cross_button.png'
import darkModeButton from '/public/assets/ui/dark_mode.png'

let props = defineProps(['props'])
const emits = defineEmits(['filtersChange'])

let filters = toRefs(props)
let darkMode = inject('darkMode')

let state = ref(false)
const searchBarRef = ref()
let throttle_search = false

function swap_filter(filter, target, checkbox, button) {

  // console.log('swapping filter', filter, target, checkbox, button)

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
  emits('filtersChange', filters)
}

function search_bar(event) {
  filters['search_bar'] = event
  emits('filtersChange', filters)

  // let timeOutId = 0
  //
  // if (throttle_search === false) {
  //   throttle_search = true
  //
  //   timeOutId = setTimeout(function () {
  //     filters['search_bar'] = event
  //     emits('filtersChange', filters)
  //     throttle_search = false
  //   }, 10)
  //
  // }
  //
  // if (event === "") {
  //   clearTimeout(timeOutId)
  //   filters['search_bar'] = event
  //   emits('filtersChange', filters)
  //   throttle_search = false
  // }
}


onMounted(() => {
  filters = filters.props.value
})

</script>
<template>
  <div :class="darkMode ? 'dark_light ': ''">
    <div class="filters_nav_wrapper">
      <div class="filter_button_wrapper" @click="state = !state">
        <h1>Filters</h1>
        <img :class="darkMode ? 'dark_image ': ''" :src="filterButton" alt="filter button" style="width: 15px">
      </div>

      <div class="search_bar_wrapper">
        <label for="search_bar">Search</label>
        <input ref="searchBarRef" :class="darkMode ? 'search_bar dark_accent' : 'search_bar'" type="search"
               id="search_bar"
               @input="search_bar($event.target.value)">
        <img :class="darkMode ? 'dark_image ': ''" :src="crossButton" alt="cross button"
             @click="searchBarRef.value='';search_bar('')"
             style="margin-left: -27px; width: 12px; padding: 5px">
      </div>

      <div class="dark_mode_wrapper" @click="darkMode = !darkMode">
        <h1>Dark mode</h1>
        <img :class="darkMode ? 'dark_image ': ''" :src="darkModeButton" alt="dark mode button" style="width: 15px">
      </div>

    </div>

    <Collapse :when="state" class="collapse">
      <div class="filter_wrapper" v-if="filters">
        <div class="filters">
          <div class="filter_types" v-for="elem in filters" :key="elem['name']">
            <p>{{ props.value }}</p>
            <h1 class="filter_heading">{{ elem['name'] }}</h1>
            <div v-for="(filter,index) in elem['available']" :key="filter" class="filter_content_list">
              <label class="filter_label">
                <input :type="elem['checkbox'] ? 'checkbox' : 'radio'" :name="elem['name']" style="cursor: pointer"
                       :checked="elem['filter'].includes(filter)"
                       @click="swap_filter(filter,elem['filter'],elem['checkbox'],$event)">
                {{ elem['display'][index] }}
              </label>
            </div>
          </div>
        </div>
      </div>
    </Collapse>
  </div>

</template>

<style scoped>
.filters_nav_wrapper {
  display: flex;
  flex-flow: row;
  justify-content: center;
  align-items: center;
  padding: 5px;
  height: 30px;
  font-size: 0.9em;

  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);
  gap: 20px;
}

.dark .filters_nav_wrapper {
  box-shadow: 0 0 8px rgba(0, 0, 0, 1);
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
  align-items: center;
  gap: 5px;
}

.filters {
  /*font-family: Calibri, serif;*/
  user-select: none;
  font-size: 1em;
  font-weight: lighter;

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

.filter_heading {
  text-decoration: underline;
  font-weight: normal;
  padding-bottom: 5px;
  padding-top: 5px;
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
  border-width: 0;
  padding: 8px;
  cursor: pointer;
  user-select: none;
  display: flex;
  gap: 5px;
  align-items: center;
}

.search_bar {
  height: 20px;
  border-radius: 5px;
  border-width: 2px;
  outline: none;
  padding: 2px;
}

.dark_mode_wrapper {
  /*outline: 1px solid red;*/
  align-items: center;
  padding: 12px;
  cursor: pointer;
  user-select: none;
  display: flex;
  flex-flow: row wrap;
  gap: 5px;
}
</style>