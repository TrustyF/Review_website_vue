<script setup>
import {defineProps, defineEmits, ref, watch, onMounted, computed} from 'vue'
import asset_paths from '../../public/assets/tags/assets.json'
import axios from 'axios'
import TagContainer from "@/components/MovieContainer/TagContainer";

const props = defineProps(['data', 'open'])
let MovChanges = {}

const editConfirmed = ref(false)

const iconTitle = ref("")
const iconDesc = ref("")
const iconImg = ref("")
const iconTier = ref("")

// const availableTypes = ["movie", "tv", "documentary"]
const availableRegions = ["western", "asian"]
const availableTiers = ["cyan", "gold", "green", "purple", "red", "silver"]

function addChange(target, change) {
  console.log(target, change)
  console.log(MovChanges)
  MovChanges[target] = change
}

function pushChange() {
  axios.post("http://localhost:5000/edit_movie/", {'newData': MovChanges, 'oldData': props.data})
      .then(response => {
        console.log("edit status", response.status)
      })
}

</script>
<template>
  <div class="main_win">
    <div class="metadata box_wrapper">
      <p>{{ data.title }}</p>

      <!--      Rating-->
      <label for="rating_input">Rating</label>
      <input type="number" id="rating_input" :value="data['my_rating']"
             @change="addChange('my_rating',String($event.target.value))">
      <!--      Region-->
      <label for="region">Region</label>
      <form id="region" @change="addChange('region',String($event.target.value))">
        <select>
          <option v-for="elem in availableRegions" :key="elem">{{ elem }}</option>
        </select>
      </form>

    </div>

    <div class="upload box_wrapper">
      <button @click="pushChange">upload changes</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "DbHelper"
}
</script>

<style>
.box_wrapper {
  width: 200px;
  display: flex;
  flex-flow: column;
  align-items: flex-start;
  gap: 5px;

  background-color: white;

  border: 1px solid black;
  border-radius: 5px;

  padding: 5px;
  margin: 5px;
}
</style>