<script setup>
import TagContainer from "@/components/TagContainer";
import MovieContainer from "@/components/MovieContainer";
import asset_paths from '../../public/assets/tags/assets.json'

</script>
<template>
  <div v-if="open" class="db_helper">
    <div class="load_movie">
      <div class="wrapper">
        <div class="wrapper">
          <div>

            <!--            <MovieContainer :data="data"></MovieContainer>-->

            <h1 style="padding: 10px">{{ data['title'] }}</h1>

            <div>
              <label>Rating</label>
              <input type="number" :value="data['my_rating']" @change="data['my_rating'] = $event.target.value">
            </div>

            <!--            <div>-->
            <!--              <label style="padding: 10px" @change="data['difficulty'] = $event.target.value">Difficulty</label>-->
            <!--              <input type="number" value="2">-->
            <!--            </div>-->

            <div>
              <button v-if="confirmed === false" style="margin: 10px" type="button" @click="editData">Confirm</button>
              <button style="margin: 10px" type="button" @click="pushData">Push</button>
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
        <span>----------------</span>
        <button type="button" @click="addPreset">Add to presets</button>
        <button type="button" @click="removePreset">Remove from presets</button>
        <span>----------------</span>

        <div v-if="asset_paths">
          <button type="button" @click="iconTier=tier" v-for="tier in availableTiers" :key="tier"
                  :style="`background:${tier};border-radius: 5px;padding:5px`">{{ tier }}
          </button>
        </div>
      </div>

      <div id="icons_selector">
        <button type="button" v-for="asset in asset_paths['icons'][iconTier]" :key="asset" :name="asset"
                class="icon_button" @click="iconId=asset">
          <img :key="asset" v-lazy="`./assets/tags/icons/${iconTier}/${asset}`" class="icon_image" alt="icon">
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
// import asset_paths from '../../public/assets/tags/assets.json'

export default {
  name: "DbHelper",
  props: {
    open: Boolean,
    inputData: {},
  },
  watch: {
    inputData: function (newVal, oldVal) {
      console.log(newVal)
      this.data = this.inputData
      this.confirmed = false
    }
  },
  data() {
    return {
      data: {},
      availableTiers: ['gold', 'green', 'silver', 'red', 'purple', 'cyan'],
      iconId: "",
      iconTier: "gold",
      iconTitle: "",
      iconDesc: "",
      confirmed: false,
    }
  },
  methods: {
    editData() {
      axios.post('http://localhost:5000/edit_movie/', this.data)
          .then(response => {
            if (response.status === 200) this.confirmed = true
          })
          .catch(error => {
          })
    },
    pushData() {
      axios.get('http://localhost:5000/push_movie/')
          .catch(error => {
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
  top: 490px;

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
  height: 400px;
  gap: 10px;
}

#icon_description {
  outline: 1px solid grey;
  padding: 5px;
  max-width: 150px;
  /*display: flex;*/
  /*flex-flow: column;*/
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