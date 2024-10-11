<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import {get_current_user} from "@/firebase_auth.js";

const curr_api = inject("curr_api");
let selected_media = inject('selected_media')

let available_tier_lists = ref([])
let dragged_tier_list = ref()

let new_list_name = ref()

async function fetch_tier_lists() {
  const url = new URL(`${curr_api}/user_list/get`)

  const result = await fetch(url).then(response => response.json())

  available_tier_lists.value = result.sort((a,b)=>b['count'] - a['count'])
}

async function add_new_list() {
  if (new_list_name.value === undefined || new_list_name.value === '') return

  const token = await get_current_user()


  const url = new URL(`${curr_api}/user_list/add`)
  url.searchParams.set('name', new_list_name.value)

  await fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': token.uid,
      'Content-Type': 'application/json',
    }
  }).then(response => response.json())
  await fetch_tier_lists()
}

function allowDrop(event) {
  event.preventDefault();
}

function add_drop_to_media() {

  if (selected_media.value['user_lists'].map((e) => e.id).includes(dragged_tier_list.value['id'])) return
  selected_media.value['user_lists'].push(dragged_tier_list.value)
}

function remove_drop_from_media() {
  let index = selected_media.value['user_lists'].map((elem) => elem['id']).indexOf(dragged_tier_list.value['id'])

  if (index > -1) {
    selected_media.value['user_lists'].splice(index, 1)
  }
}

function drag(data) {
  dragged_tier_list.value = data
}

onMounted(() => {
  fetch_tier_lists()
})
</script>

<template>
  <div class="tier_list_wrapper">

    <div class="tier_list_grab_area">

      <div class="current_tier_lists" @dragover="allowDrop" @drop="add_drop_to_media"
           @dragleave="remove_drop_from_media">
        <div class="tier_list_box" draggable="true" @dragstart="drag(t)" v-for="t in selected_media['user_lists']"
             :key="t['id']">
          {{ t['name'] }}
        </div>
      </div>

      <div class="available_tier_lists">
        <div class="tier_list_box" draggable="true" @dragstart="drag(t)" v-for="t in available_tier_lists"
             :key="t['id']">
          {{ t['name'] }}
          <p style="font-size: 0.6em;position: absolute;left: 0;top: 0;padding: 3px">{{t['count']}}</p>
        </div>
      </div>

    </div>

    <div class="tier_list_updates">
      <input v-model="new_list_name" placeholder="new user">
      <button @click="add_new_list()">Add</button>
    </div>

  </div>


</template>

<style scoped>
.tier_list_wrapper {
  padding: 10px;
  height: 100%;
  border: 2px dotted #464646;
  display: flex;
  flex-flow: column nowrap;
  gap: 10px;
}

.tier_list_grab_area {
  /*padding: 10px;*/
  height: 90%;
  display: flex;
  gap: 10px;
}

.current_tier_lists {
  display: flex;
  flex-flow: column;
  gap: 5px;
  padding: 10px;
  border: 1px solid #464646;
  min-width: 100px;
}

.available_tier_lists {
  display: flex;
  flex-flow: column;
  gap: 5px;
  min-width: 100px;
  padding: 10px;
  border: 1px solid #464646;
  overflow-y: scroll;
}

.tier_list_box {
  position: relative;
  text-align: center;
  font-size: 0.7em;
  cursor: grab;
  border-radius: 5px;
  padding: 10px;
  background-color: #41404d;
}

.tier_list_updates {
  display: flex;
  gap: 5px;
}
</style>