<script setup>
import {defineProps, defineEmits, ref, watch} from 'vue'
import asset_paths from '../../public/assets/tags/assets.json'
import axios from 'axios'
import TagContainer from "@/components/MovieContainer/TagContainer";

const props = defineProps(['data', 'open'])

const currentMovie = ref({})
const editConfirmed = ref(false)

const iconTitle = ref("")
const iconDesc = ref("")
const iconImg = ref("")
const iconTier = ref("")

const availableTiers = ref(["cyan", "gold", "green", "purple", "red", "silver"])


watch(props, (newVal, oldVal) => {
  currentMovie.value = props['data']
})

watch(iconTier, (newVal, oldVal) => {
  console.log('new', newVal)
})

function editData() {
  axios.post('http://localhost:5000/edit_movie/', {
    oldData: this.data,
    newRating: this.newRating
  }).then((response) => {
    if (response.status === 200) {
      editConfirmed.value = true
    }
  })
}
</script>
<template>
  <div v-if="props['open']" class="db_helper">
    <div class="load_movie">
      <div class="wrapper">
        <div class="wrapper">
          <div>
            <!--            <MovieContainer :data="data"></MovieContainer>-->

            <h1 style="padding: 10px">{{ currentMovie['title'] }}</h1>
            <div>
              <label>Rating</label>
              <input type="number" :value="currentMovie['my_rating']"
                     @change="currentMovie['my_rating'].value = $event.target.value">
            </div>

            <div>
              <button v-if="!editConfirmed" style="margin: 10px" type="button" @click="editData">Confirm</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="wrapper" id="icon_adder">

      <div id="icon_description">

        <div style="width: min-content">
          <img :src="`./assets/tags/icons/${iconTier}/${iconImg}`" class="icon_image" alt="icon">
        </div>

        <label>Title </label>
        <input type="text" v-model="iconTitle"/>

        <label>Description </label>
        <input type="text" v-model="iconDesc"/>

        <!--        <button type="button" @click="addIcon">Add to movie</button>-->
        <!--        <button type="button" @click="removeIcon">Remove from movie</button>-->

        <!--        <button type="button" @click="addPreset">Add to presets</button>-->
        <!--        <button type="button" @click="removePreset">Remove from presets</button>-->

      </div>

      <div id="tier_selector" v-if="asset_paths">
        <button type="button" v-for="tier in availableTiers" :key="tier" @click="iconTier.value=tier"
                :style="`background:${tier};border-radius: 5px;padding:5px`">{{ tier }}
        </button>
      </div>

      <div id="icons_selector">
        <button type="button" v-for="asset in asset_paths['icons'][iconTier]" :key="asset" :name="asset"
                class="icon_button" @click="iconImg.value=asset">
          <img :key="asset" v-lazy="`./assets/tags/icons/${iconTier}/${asset}`" class="icon_image"
                         alt="icon">
        </button>
      </div>

      <button @click="this.$emit('settingsClosed', false)">x</button>

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
  /*border-style: solid;*/
  position: fixed;
  display: flex;
  z-index: 10;
  bottom: 0;
  width: 1500px;
  height: 270px;

  /*background-color: green;*/
}

.wrapper {
  padding: 10px;
  margin: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.75);
  background-color: white;
}

.load_movie {
  display: flex;
}

#movie_properties {
  display: flex;
  /*grid-template-rows: repeat(3,1fr);*/
}

#icon_adder {
  display: flex;
  grid-template-columns: repeat(3, 1fr);
  /*justify-content: space-evenly;*/
  /*height: 400px;*/
  gap: 10px;
}

#icon_description {
  outline: 1px solid grey;
  padding: 5px;
  max-width: 300px;
  display: flex;
  flex-flow: column;
}

#tier_selector {
  display: flex;
  flex-flow: column;
  /*width: 100px;*/
}

#icons_selector {
  outline: 1px solid grey;
  padding: 5px;
  width: 100%;
  /*height: 100%;*/
  /*margin: auto;*/
  overflow-y: scroll;
  scroll-behavior: smooth;
}

#icons_preset {
  outline: 1px solid grey;
  padding: 5px;
  width: 50%;
  /*height: 100%;*/
  /*margin: auto;*/
  /*overflow-y: scroll;*/
  scroll-behavior: smooth;
}

.icon_button {
  /*border-style: solid;*/
  margin: 2px;

}

.icon_image {
  /*border-style: solid;*/
  width: 50px;

}
</style>