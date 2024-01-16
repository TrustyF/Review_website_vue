<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["data","text_size","text_limit"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

function add_line_breaks(content) {
  let replaced = content
  // let regEx = new RegExp(/(.{10}[^ ]* )/g)
  let regEx = new RegExp(/(.{30}[^ ]* )/g)
  replaced = replaced.replace(regEx, "$1\n")
  // replaced = replaced.replace(/\./g, `\n`)

  return replaced
}

function add_line_break_v2(content){
  return content
}
</script>

<template>
  <div ref="tooltip_container" class="tag_tooltip" v-if="data!==undefined">

    <img class="tag_preview" :src="`/tags/icons/${data['tier']}/${data['image_path']}`">

    <div class="tooltip_content">
      <h1 class="title">{{ data['name'] }}</h1>
      <h1 class="description">{{ add_line_break_v2(data['overview']) }}</h1>
    </div>

    <div class="tag_tooltip_arrow"></div>

  </div>
  <div v-else class="tag_tooltip">no data</div>

</template>

<style scoped>
.tag_tooltip {
  /*position: absolute;*/
  overflow: hidden;
  /*background: linear-gradient(to left, #41404d 60%, #605c57 100%);*/

  box-shadow: 0 0 calc(v-bind(text_size) * 8px) #191726;
  border-radius: calc(v-bind(text_size) * 50px);
  background-color: #2b2a34;

  z-index: 300;

  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  gap: calc(v-bind(text_size) * 10px);

  /*height: calc(v-bind(text_size) * 4em);*/

  opacity: 0;
  visibility: hidden;
  transition: 300ms;
}

.tag_tooltip:after {
  content: "";
  height: 100%;
  padding: 0 calc(v-bind(text_size) * 15px) 0 0;
}

.tag_tooltip_arrow {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -10px;
  border-width: 10px;
  border-style: solid;
  border-color: #2b2a34 transparent transparent transparent;
}

.tooltip_content {
  display: flex;
  flex-flow: column nowrap;
  gap: calc(v-bind(text_size) * 4px);
  padding: calc(v-bind(text_size) * 10px) 0 calc(v-bind(text_size) * 10px) 0;
}

.title {
  font-size: calc(v-bind(text_size) * 1em);
  font-weight: 700;
  /*color: black;*/
  text-shadow: 1px 1px calc(v-bind(text_size) * 3px) black, 0 0 calc(v-bind(text_size) * 5px) black;
}

.description {
  font-size: calc(v-bind(text_size) * 0.8em);
  color: #b0b0b0;
  text-shadow: 0 0 calc(v-bind(text_size) * 7px) black;
  /*word-break: break-word;*/
}

.tag_preview {
  height: calc(v-bind(text_size) * 4em);
  /*width: 100%;*/
  filter: drop-shadow(0 0 calc(v-bind(text_size) * 5px) rgba(0, 0, 0, 0.75));
}
</style>