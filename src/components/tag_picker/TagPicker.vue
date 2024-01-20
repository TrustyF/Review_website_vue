<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import Badge from "@/components/media_container/movie_container/sub_components/badge.vue";


let props = defineProps(["media_ref", "media_type"]);
let emits = defineEmits(["tags"]);
const curr_api = inject("curr_api");

const folders = Object.keys(import.meta.glob('/public/tags/icons/**'));
const tiers = [...new Set(folders.map((elem) => elem.split('/')[4]))]

const tag_images = ref({})

let available_badges = ref()
let constructed_badges = ref([])
let dragged_badge = ref()

const temp_tag_template = {
  'name': null,
  'overview': null,
  'tier': null,
  'origin': props['media_type'],
  'image_path': null,
}
let temp_tag = ref(temp_tag_template)

async function get_tags() {
  const url = new URL(`${curr_api}/tag/get`)

  let result = await fetch(url).then(response => response.json())

  available_badges.value = result.sort((a, b) => a['image_path'] > b['image_path'])
  available_badges.value = Object.groupBy(result, ({tier}) => tier)
  console.log(result)
}

function map_images_from_folders() {

  tiers.forEach((tier) => {
    tag_images.value[tier] = []
  })

  folders.forEach((path) => {
    let tier = path.split('/')[4]
    let name = path.split('/')[5]
    tag_images.value[tier].push(name)
  })
}

function allowDrop(event) {
  event.preventDefault();
}

function drag(data) {
  console.log(data)
  dragged_badge.value = data
}

function add_dragged_badge_to_constructor() {
  constructed_badges.value.push(dragged_badge.value)
}

function remove_dragged_badge_from_constructor() {
  let index = constructed_badges.value.map((elem) => elem['id']).indexOf(dragged_badge.value['id'])
  console.log(constructed_badges.value.map((elem) => elem['id']), dragged_badge.value['id'], index)

  if (index > -1) {
    constructed_badges.value.splice(index, 1)
  }
}

function add_dragged_badge_to_editor() {
  temp_tag.value = dragged_badge.value
}

function switch_tag_image(path) {
  temp_tag.value['image_path'] = path
}

async function add_tag() {
  const url = new URL(`${curr_api}/tag/add`)

  await fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(temp_tag.value)
  }).then(response => response.json())

  await get_tags()
}

async function update_tag() {
  const url = new URL(`${curr_api}/tag/update`)

  await fetch(url, {
    method: 'POST',
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(temp_tag.value)
  }).then(response => response.json())

  await get_tags()
}

async function delete_tag() {
  const url = new URL(`${curr_api}/tag/delete`)

  url.searchParams.set('id', temp_tag.value['id'])

  await fetch(url).then(response => response.json())
  temp_tag.value = temp_tag_template

  await get_tags()
}

function emit() {
  emits('tags', constructed_badges.value)
}

onMounted(() => {
  get_tags()
  map_images_from_folders()
})

watch(props, (newV) => {
  if (newV.media_ref.tags === null) {
    newV.media_ref.tags = []
  }
  constructed_badges.value = newV.media_ref.tags
})
</script>

<template>
  <div class="tag_picker_wrapper">

    <div class="top_area">
      <div style="display: flex;flex-flow: column">
        <div class="tag_constructor" @dragover="allowDrop" @dragleave="remove_dragged_badge_from_constructor"
             @drop="add_dragged_badge_to_constructor">
          <badge @dragstart="drag(tag)" :data="tag" v-for="tag in constructed_badges" :key="tag.id" :min_size="200"
                 :show_title="true"></badge>
        </div>
        <button @click="emit">Push to media</button>
      </div>

      <div class="tag_editor" @dragover="allowDrop" @drop="add_dragged_badge_to_editor">
        <badge :data="temp_tag" :min_size="200" :show_title="true"></badge>
        <div class="editor_form">

          <div class="form_box" v-for="key in Object.keys(temp_tag)" :key="key">
            <label v-if="key!=='id'" :for="key">{{ key }}</label>

            <textarea v-if="key==='overview'" :id="key" v-model="temp_tag[key]" rows="5"></textarea>
            <select v-else-if="key==='tier'" v-model="temp_tag[key]">
              <option v-for="tier in tiers" :key="tier" :selected="tier.indexOf(temp_tag[key])+1">{{ tier }}</option>
            </select>
            <input v-else-if="key!=='id'" :id="key" v-model="temp_tag[key]">

          </div>

        </div>
        <div class="editor_buttons">
          <button @click="add_tag">add tag</button>
          <button @click="update_tag">update tag</button>
          <button @click="delete_tag">delete tag</button>
        </div>
      </div>

      <div class="badges_wrapper">
        <div style="display:flex;flex-flow: row wrap;gap: 2px;" v-for="tier in available_badges" :key="tier.id">
          <badge @dragstart="drag(badge)" :data="badge" v-for="badge in tier" :key="badge.id"
                 :min_size="200"></badge>
        </div>
      </div>
    </div>

    <div class="bottom_area">
      <div class="available_images">
        <div class="template_image" @click="switch_tag_image(img)" v-for="img in tag_images[temp_tag['tier']]"
             :key="img">
          <img class="tag_template_image" :src="`/public/tags/icons/${temp_tag['tier']}/${img}`" alt="tag_template">
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.tag_picker_wrapper {
  border: 2px dotted #464646;
  padding: 10px;
  display: flex;
  flex-flow: column;
  gap: 10px;
}

.top_area {
  display: flex;
  flex-flow: row;
  justify-content: space-between;
  gap: 20px;
}

.tag_constructor {
  border: 1px solid #464646;
  padding: 10px;
  display: flex;
  flex-flow: column nowrap;
  gap: 10px;
  width: 150px;
  flex-grow: 1;
}

.tag_editor {
  border: 1px solid #464646;
  padding: 10px;
  display: flex;
  flex-flow: column nowrap;
  gap: 10px;
  width: 300px;
}

.editor_buttons {
  display: flex;
  gap: 10px;
}

.editor_form {
  display: flex;
  flex-flow: column;
  gap: 10px;
}

.form_box {
  display: flex;
  flex-flow: column;
  gap: 3px;
}

.badges_wrapper {
  border: 1px solid #464646;
  padding: 10px;
  display: flex;
  flex-flow: column;
  gap: 10px;
  width: 50%;
  /*height: 200px;*/
  /*overflow-y: scroll;*/
}

.bottom_area {

}

.available_images {
  display: flex;
  flex-flow: row wrap;
  gap: 5px;
  border: 1px solid #464646;
  padding: 10px;
}

.tag_template_image {
  width: 50px;
}
</style>