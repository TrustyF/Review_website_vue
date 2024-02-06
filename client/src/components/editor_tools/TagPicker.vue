<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import Badge from "@/components/media_container/movie_container/sub_components/badge.vue";
import {get_current_user} from "@/firebase_auth.js";
import axios from "axios";

let selected_media = inject('selected_media')

let props = defineProps(["media_type"]);
let emits = defineEmits(["tags"]);
const curr_api = inject("curr_api");

const tiers = ['gold', 'green', 'purple', 'grey', 'red']

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

  // available_badges.value = result.sort((a, b) => a['image_path'] > b['image_path'])
  available_badges.value = result.sort((a, b) => a['count'] < b['count'])
  available_badges.value = Object.groupBy(result, ({tier}) => tier)
  available_badges.value = Object.values(available_badges.value)

  // sort tags by color
  const priority = ['gold', 'green', 'purple', 'silver', 'red']
  available_badges.value.sort((a, b) => {
    const fi = priority.indexOf(a[0].tier)
    const si = priority.indexOf(b[0].tier)
    return fi - si
  })
}

async function get_tier_images() {

  const url = `${curr_api}/tag/get_tier_images`
  const params = {
    tier: temp_tag.value.tier
  }

  const result = await axios.get(url, {params: params})
      .then(response => response.data)

  console.log(result)
  tag_images.value = result
}

function allowDrop(event) {
  event.preventDefault();
}

function drag(data) {
  dragged_badge.value = data
}

function add_dragged_badge_to_constructor() {
  constructed_badges.value.push(dragged_badge.value)
}

function remove_dragged_badge_from_constructor() {
  let index = constructed_badges.value.map((elem) => elem['id']).indexOf(dragged_badge.value['id'])

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
  const token = await get_current_user()

  const url = new URL(`${curr_api}/tag/add`)


  await fetch(url, {
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
      'Authorization': token.uid,
    },
    body: JSON.stringify(temp_tag.value)
  }).then(response => response.json())

  await get_tags()
}

async function update_tag() {
  const token = await get_current_user()

  const url = new URL(`${curr_api}/tag/update`)

  await fetch(url, {
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
      'Authorization': token.uid,
    },
    body: JSON.stringify(temp_tag.value)
  }).then(response => response.json())

  await get_tags()
}

async function delete_tag() {
  const token = await get_current_user()

  const url = new URL(`${curr_api}/tag/delete`)

  url.searchParams.set('id', temp_tag.value['id'])

  await fetch(url, {
    method: 'GET',
    headers: {
      "Content-Type": "application/json",
      'Authorization': token.uid,
    }
  }).then(response => response.json())
  temp_tag.value = temp_tag_template

  await get_tags()
}

function emit() {
  emits('tags', constructed_badges.value)
}

onMounted(() => {
  get_tags()

  if (selected_media.value.tags === null) {
    selected_media.value.tags = []
  }
  constructed_badges.value = selected_media.value.tags
})
</script>

<template>
  <div class="tag_picker_wrapper">

    <div class="top_area">
      <div style="display: flex;flex-flow: column">
        <div class="tag_constructor" @dragover="allowDrop" @dragleave="remove_dragged_badge_from_constructor"
             @drop="add_dragged_badge_to_constructor">
          <badge @dragstart="drag(tag)" :data="tag" v-for="tag in constructed_badges" :key="'constructor'+tag.id"
                 :min_size="200"
                 :show_title="true"></badge>
        </div>
        <button @click="emit">Push to media</button>
      </div>

      <div class="tag_editor" @dragover="allowDrop" @drop="add_dragged_badge_to_editor">
        <badge :data="temp_tag" key="tag_editor_badge" :min_size="200" :show_title="true"></badge>
        <div class="editor_form">

          <div class="form_box">

            <label for="tag_name">Name</label>
            <input id="tag_name" v-model="temp_tag['name']">

            <label for="tag_overview">Overview</label>
            <textarea id="tag_overview" v-model="temp_tag['overview']"></textarea>

            <label for="tag_tier">Tier</label>
            <select id="tag_tier" v-model="temp_tag['tier']" @change="get_tier_images">
              <option v-for="tier in tiers" :key="tier" :selected="tier.indexOf(temp_tag['tier'])+1">{{ tier }}</option>
            </select>

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

          <div v-for="badge in tier" :key="'available'+badge.id">
            <div class="badge_count">{{ badge.count }}</div>
            <badge @dragstart="drag(badge)" :data="badge"
                   :min_size="200"></badge>
          </div>

        </div>
      </div>
    </div>

    <div class="bottom_area">
      <div class="available_images">
        <div class="template_image" @click="switch_tag_image(img)" v-for="img in tag_images"
             :key="img">
          <img class="tag_template_image" :src="`${curr_api}/tag/get_image?tier=${img[0]}&path=${img[1]}`"
               alt="tag_template">
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
  margin-top: auto;
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
  position: relative;
  border: 1px solid #464646;
  padding: 10px;
  display: flex;
  flex-flow: column;
  gap: 10px;
  width: 50%;
  /*height: 200px;*/
  /*overflow-y: scroll;*/
}

.badge_count {
  position: absolute;
  z-index: 10;
  width: 10px;
  height: 10px;
  font-size: 7px;
  /*border-radius: 50%;*/
  /*text-align: center;*/
  /*background-color: grey;*/
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