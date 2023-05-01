<script setup>
import TagContainer from "@/components/MovieContainer/TagContainer";
import MovieContainer from "@/components/MovieContainer/MovieContainer";
import asset_paths from '../../public/assets/tags/assets.json'

</script>
<template>
  <div v-if="isOpen" class="db_helper">
    <div class="load_movie">
      <div class="wrapper">
        <div class="wrapper">
          <div>

            <!--            <MovieContainer :data="data"></MovieContainer>-->

            <h1 style="padding: 10px">{{ data['title'] }}</h1>

            <div>
              <label>Rating</label>
              <input type="number" :value="data['my_rating']" @change="newRating = $event.target.value">
            </div>

            <!--            <div>-->
            <!--              <label style="padding: 10px" @change="data['difficulty'] = $event.target.value">Difficulty</label>-->
            <!--              <input type="number" value="2">-->
            <!--            </div>-->

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
          <img :src="`./assets/tags/icons/${iconTier}/${iconId}`" class="icon_image" alt="icon">
        </div>

        <label>Title </label>
        <input type="text" v-model="iconTitle"/>

        <label>Description </label>
        <input type="text" v-model="iconDesc"/>

        <button type="button" @click="addIcon">Add to movie</button>
        <button type="button" @click="removeIcon">Remove from movie</button>

        <button type="button" @click="addPreset">Add to presets</button>
        <button type="button" @click="removePreset">Remove from presets</button>

      </div>

      <div id="tier_selector" v-if="asset_paths">
        <button type="button" @click="iconTier=tier" v-for="tier in availableTiers" :key="tier"
                :style="`background:${tier};border-radius: 5px;padding:5px`">{{ tier }}
        </button>
      </div>

      <div id="icons_selector">
        <button type="button" v-for="asset in asset_paths['icons'][iconTier]" :key="asset" :name="asset"
                class="icon_button" @click="iconId=asset">
<!--          <tag-container :key="asset" v-lazy="`./assets/tags/icons/${iconTier}/${asset}`" class="icon_image" alt="icon"></tag-container>-->
        </button>
      </div>

      <button @click="this.$emit('settingsClosed', false)" style="position: absolute; right: 0">x</button>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {reactive} from "vue"
// import asset_paths from '../../public/assets/tags/assets.json'

export default {
  name: "DbHelper",
  props: {
    inputData: Object,
    isOpen: Boolean
  },
  watch: {
    inputData: function (newVal, oldVal) {
      console.log(newVal)
      this.data = this.inputData
    },
    isOpen: function (newVal, oldVal) {
      console.log(newVal)
      this.opened = this.isOpen
    },

  },
  data() {
    return {
      data: {},
      opened:false,
      availableTiers: ['gold', 'green', 'silver', 'red', 'purple', 'cyan'],
      iconId: "",
      iconTier: "gold",
      iconTitle: "",
      iconDesc: "",

      newRating: Number,
      editConfirmed:false
    }
  },
  methods: {
    editData() {
      axios.post('http://localhost:5000/edit_movie/', {
        oldData: this.data,
        newRating: this.newRating
      }) .then((response) =>{
        if (response.status === 200){
          this.editConfirmed = true
        }
      })
    }
  }

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