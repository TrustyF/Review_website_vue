<script setup>
import {onBeforeMount, onMounted, reactive, ref, watch} from "vue";
import {database, img_database} from "@/firebase";
import {collection, query, where, orderBy, getDocs, limit, doc, addDoc, deleteDoc, updateDoc} from "firebase/firestore";
import {getDownloadURL, ref as storageRef, uploadBytesResumable, updateMetadata} from "firebase/storage";

import MovieContainer from "@/components/MovieContainer";
import TagContainer from "@/components/TagContainer";

import asset_paths from '../../public/assets/tags/assets.json'
import '../styles/db_helper.css'

const movie_db = collection(database, 'movies')
const tags_db = collection(database, 'tag_presets')

const tag_presets = ref()
const iconTitle = ref("")
const iconDesc = ref("")
const iconImg = ref()
const iconTier = ref("gold")
const movieId = ref("")
const presetId = ref("")

function readJson(input) {
  const file = input.target.files[0]
  const blob = new Blob([file], {type: "application/json"});
  const reader = new FileReader()

  reader.readAsText(blob)

  reader.onload = () => {
    console.log("res", JSON.parse(reader.result))
    movie.value = JSON.parse(reader.result)
    console.log('Movie', movie.value)
  }

}

async function queryFirebase(input) {
  let search = input.target.value

  let words = search.split(" ")
  for (let i = 0; i < words.length; i++) {
    words[i] = words[i][0].toUpperCase() + words[i].substr(1)
  }
  words = words.join(" ")
  console.log(words)

  const ref = collection(database, 'movies')
  const q = query(ref, where("name", ">=", words), limit(1))
  const querySnapshot = await getDocs(q)

  // const response = querySnapshot.docs[0].data()

  movieId.value = querySnapshot.docs[0].id
  movie.value = querySnapshot.docs[0].data()
}

function pushImageToStorage(input) {
  input.preventDefault()
  const file = input.target.files[0]
  const imageRef = storageRef(img_database, 'movie_posters/' + file.name)

  console.log("pushing image to db", file)

  uploadBytesResumable(imageRef, file)
      .then((snapshot) => {
        getDownloadURL(snapshot.ref).then((url) => movie.value['image'] = url)
      })
}

async function getImageFromStorage(input) {
  const url = await getDownloadURL(storageRef(img_database, input))
  console.log("url", url)
  return url
}

function pushToDb(input) {
  console.log("pushToDb", movie.value)
  addDoc(movie_db, movie.value)
}

function modifyToDb(input) {
  console.log("modifyToDb", movie.value)
  updateDoc(doc(movie_db, movieId.value), movie.value)
}

function addIcon(input) {
  console.log("addIcon", movie.value)

  if (movie.value["tags"] === undefined) {
    console.log("tags defined")
    movie.value["tags"] = []
  }

  if (iconTitle.value && iconDesc.value && iconImg.value) {
    movie.value["tags"].push({
      "name": iconTitle.value,
      "path": iconImg.value,
      "description": iconDesc.value
    })
    modifyToDb()
  }
}

function removeIcon(input) {
  console.log("removeIcon", iconTitle.value, movie.value)

  if (iconTitle.value) {
    const elem = (elem) => elem['name'] === iconTitle.value
    const index = movie.value['tags'].findIndex(elem)
    console.log("index", index)
    movie.value['tags'].splice(index, 1)
    modifyToDb()
  }
}

function selectPreset(input) {
  console.log("selectPreset", input)

  iconTitle.value = input['name']
  iconDesc.value = input['description']
  iconImg.value = input['path']
  presetId.value = input['id']
}

async function addPreset() {
  console.log("addPreset")
  if (iconTitle.value && iconDesc.value && iconImg.value) {
    await addDoc(tags_db, {
          "name": iconTitle.value,
          "path": iconImg.value,
          "description": iconDesc.value,
          "tier": iconTier.value
        }
    )
    await loadPresets()
  }
}

async function removePreset() {
  console.log("removePreset", presetId.value)

  if (presetId.value) {
    console.log(presetId.value)
    await deleteDoc(doc(tags_db, presetId.value))
    await loadPresets()
  }
}

async function loadPresets() {
  const q = query(tags_db, where('tier', '==', iconTier.value))
  const querySnapshot = await getDocs(q)
  const response = querySnapshot.docs.map(elem => {
    const out = elem.data()
    out['id'] = elem.id
    return out
  })
  console.log("loadPresets", response)
  tag_presets.value = response
}

loadPresets()

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