<script setup>
import {defineProps, defineEmits, ref, watch, onMounted, computed} from 'vue'
import asset_paths from '../../public/assets/tags/assets.json'
import axios from 'axios'
import TagContainer from "@/components/MovieContainer/TagContainer";

const props = defineProps(['data', 'open'])

const MovChanges = ref({
  'my_rating': String
})
const editConfirmed = ref(false)

const iconTitle = ref("")
const iconDesc = ref("")
const iconImg = ref("")
const iconTier = ref("")

const availableTiers = ref(["cyan", "gold", "green", "purple", "red", "silver"])

function addChange(target,change){
  console.log(target,change)
  MovChanges.value[target]=change
}

</script>
<template>
  <div class="main_win">
    <div class="metadata">
      <p>{{ data.title }}</p>
      <input type="number" :value="data['my_rating']" @change="addChange('my_rating',String($event.target.value))">
      <input type="date" :value="data['my_rating']" @change="addChange('date_rated',String($event.target.value))">

    </div>
  </div>
</template>

<script>
export default {
  name: "DbHelper"
}
</script>

<style>
.db_helper {
}
</style>