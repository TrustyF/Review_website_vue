<script setup>

import MovieContainer from "@/components/MovieContainer";
import TagContainer from "@/components/TagContainer";

import asset_paths from '../../public/assets/tags/assets.json'
import '../styles/db_helper.css'

</script>
<template>
  <div class="load_movie">
    <MovieContainer class="open" :data="movie"/>
    <MovieContainer :data="movie"/>
    <div class="wrapper">

      <div class="wrapper">
        <div>
          <label style="padding: 10px">Load from Json</label>
          <input type="file" @input="readJson">
        </div>
      </div>

      <label style="padding: 10px">Modify movie
        <input type="text" @input="queryFirebase"/></label>

      <button style="margin: 10px" type="button" @click="modifyToDb">Update to database</button>

      <div class="wrapper">
        <div>
          <div>
            <label style="padding: 10px">Title</label>
            <input type="text" @input="movie['title']= $event.target.value" @change="modifyToDb">
          </div>

          <div>
            <label style="padding: 10px">Image</label>
            <input type="file" @input="movie['image'] = $event.target.files[0]" @change="modifyToDb">
          </div>

          <div>
            <label style="padding: 10px">Overview</label>
            <input type="text" @input="movie['overview']= $event.target.value" @change="modifyToDb">
          </div>

          <div>
            <label style="padding: 10px">Rating</label>
            <input type="number" @input="movie['my_rating']= parseInt($event.target.value)" @change="modifyToDb">
          </div>

<!--          <div>-->
<!--            <label style="padding: 10px">Difficulty</label>-->
<!--            <input type="number" @input="movie['difficulty']= parseInt($event.target.value)" @change="modifyToDb" value="2">-->
<!--          </div>-->

          <div>
            <button style="margin: 10px" type="button" @click="pushToDb">Add to database</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="wrapper" id="icon_adder">
    <div id="icon_description">
      <div style="width: min-content">
        <TagContainer class="preview" v-if="iconTitle || iconDesc || iconImg"
                      :tag="{'path':iconImg,'description':iconDesc,'name':iconTitle}"/>
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
        <button type="button" @click="iconTier=i; loadPresets()" v-for="(tier,i) in asset_paths['icons']" :key="tier"
                :style="`background:${i};border-radius: 5px;padding:5px`">{{ i }}
        </button>
      </div>
    </div>
    <div id="icons_preset">
      <button type="button" v-for="(tag,i) in tag_presets" :key="tag" :name="i" class="icon_button"
              @click="selectPreset(tag)">
        <TagContainer :tag="tag"/>
      </button>
    </div>
    <div id="icons_selector">
      <button type="button" v-for="asset in asset_paths['icons'][iconTier]" :key="asset" :name="asset"
              class="icon_button"
              @click="iconImg = `./assets/tags/icons/${iconTier}/` + asset">
        <img :key="asset" :src="`./assets/tags/icons/${iconTier}/` + asset" class="icon_image" alt="icon">
      </button>
    </div>
  </div>
</template>

<style>
/*.preview .top {*/
/*  visibility: visible;*/
/*  opacity: 1;*/
/*}*/
</style>