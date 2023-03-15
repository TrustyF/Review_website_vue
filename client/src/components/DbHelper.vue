<script setup>
import TagContainer from "@/components/TagContainer";
import asset_paths from '../../public/assets/tags/assets.json'
</script>
<template>
  <div v-if="open" class="db_helper">
    <div class="load_movie">
      <div class="wrapper">
        <div class="wrapper">
          <div>
            <div>
              <label style="padding: 10px">Rating</label>
              <input type="number" @change="data['my_rating'] = $event.target.value" :value="data['my_rating']">
            </div>

            <div>
              <label style="padding: 10px">Difficulty</label>
              <input type="number" value="2">
            </div>

            <div>
              <button style="margin: 10px" type="button" @click="writeJson">Confirm</button>
            </div>
          </div>
        </div>
      </div>
    </div>

<!--    <div class="wrapper" id="icon_adder">-->
<!--      <div id="icon_description">-->
<!--        <div style="width: min-content">-->
<!--          <TagContainer class="preview" v-if="iconTitle || iconDesc || iconImg"-->
<!--                        :tag="{'path':iconImg,'description':iconDesc,'name':iconTitle}"/>-->
<!--        </div>-->
<!--        <label>Title </label>-->
<!--        <input type="text" v-model="iconTitle"/>-->
<!--        <label>Description </label>-->
<!--        <input type="text" v-model="iconDesc"/>-->

<!--        <button type="button" @click="addIcon">Add to movie</button>-->
<!--        <button type="button" @click="removeIcon">Remove from movie</button>-->
<!--        <span>&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;</span>-->
<!--        <button type="button" @click="addPreset">Add to presets</button>-->
<!--        <button type="button" @click="removePreset">Remove from presets</button>-->
<!--        <span>&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;&#45;</span>-->
<!--        <div v-if="asset_paths">-->
<!--          <button type="button" @click="iconTier=i; loadPresets()" v-for="(tier,i) in asset_paths['icons']" :key="tier"-->
<!--                  :style="`background:${i};border-radius: 5px;padding:5px`">{{ i }}-->
<!--          </button>-->
<!--        </div>-->
<!--      </div>-->
<!--      <div id="icons_preset">-->
<!--        <button type="button" v-for="(tag,i) in tag_presets" :key="tag" :name="i" class="icon_button"-->
<!--                @click="selectPreset(tag)">-->
<!--          <TagContainer :tag="tag"/>-->
<!--        </button>-->
<!--      </div>-->
<!--      <div id="icons_selector">-->
<!--        <button type="button" v-for="asset in asset_paths['icons'][iconTier]" :key="asset" :name="asset"-->
<!--                class="icon_button"-->
<!--                @click="iconImg = `./assets/tags/icons/${iconTier}/` + asset">-->
<!--          <img :key="asset" :src="`./assets/tags/icons/${iconTier}/` + asset" class="icon_image" alt="icon">-->
<!--        </button>-->
<!--      </div>-->
<!--    </div>-->
  </div>
</template>

<script>
import MovieLib from "../../public/assets/movie_db_lib.json"
import axios from 'axios'

export default {
  name: "DbHelper",
  props: {
    open: Boolean,
    inputData: Object,
  },
  data() {
    return {
      data: Object,
      tag_presets: String,
      iconTitle: String,
      iconDesc: String,
      iconImg: String,
      iconTier: String,
      movieId: String,
      presetId: String,
    }
  },
  created() {
    this.data = this.inputData
  },
  methods: {
    Icons: {
      addIcon() {

      },
      removeIcon() {

      },
      addPreset() {

      },
      removePreset() {

      },
      loadPresets() {

      },
    },
    postData(){
      axios.post()
    }
  }

}
</script>

<style>
.db_helper {
  /*border-style: solid;*/
  position: absolute;
  transform: translate(-200px, 300px);
  display: flex;
  z-index: 10;

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