<script setup>
import {defineProps, defineEmits, ref, watchEffect, onMounted, watch, toRefs, inject} from 'vue'
import {Collapse} from 'vue-collapsed'
import filterButton from '/public/assets/ui/filter_button.png'
import crossButton from '/public/assets/ui/cross_button.png'

let props = defineProps(['props'])
const emits = defineEmits(['filtersChange'])

let filters = toRefs(props)

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
    <div class="filters_nav_wrapper dark_light">
      <div class="filter_button_wrapper" @click="state = !state">
        <h1>Filters</h1>
        <img class="dark_image" :src="filterButton" alt="filter button" style="width: 15px">
      </div>

      <div class="search_bar_wrapper">
        <label for="search_bar">Search</label>
        <input ref="searchBarRef" class="search_bar dark_accent" type="search"
               id="search_bar"
               @input="search_bar($event.target.value)">
        <img class="dark_image" :src="crossButton" alt="cross button"
             @click="searchBarRef.value='';search_bar('')"
             style="margin-left: -27px; width: 12px; padding: 5px">
      </div>

    </div>

<!--    <div class="filler"></div>-->

    <Collapse :when="state" class="collapse">
      <div class="filter_wrapper" v-if="filters">
        <div class="filters dark_light">
          <div class="filter_types" v-for="elem in filters"  :key="elem['name']" v-show="elem['display']!==undefined">
<!--            <p>{{ props.value }}</p>-->
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
  padding: 10px;
  /*outline: 2px solid green;*/
}

.filter_button_wrapper {
  /*outline: 1px solid red;*/
  padding: 12px 0 12px 0;
  cursor: pointer;
  user-select: none;
  display: flex;
  flex-flow: row wrap;
  align-items: center;
  gap: 5px;
}

.filters {
  /*outline: 1px solid green;*/

  user-select: none;
  font-size: 1em;
  font-weight: lighter;

  padding: 30px;
  width: fit-content;
  margin: auto;

  border-radius: 10px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  gap: 20px;

  display: flex;
  flex-flow: row wrap;
}

.filter_heading {
  /*outline: 1px red solid;*/

  text-decoration: underline;
  font-weight: normal;
  padding-bottom: 5px;
  /*padding-top: 5px;*/
}

.filter_label {
  font-size: 0.9em;
  cursor: pointer;
}

.filter_types {
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