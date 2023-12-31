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
</script>

<template>
  <div ref="tooltip_container" class="tag_tooltip">

    <img class="tag_preview" v-lazy="`/tags/icons/${data['tier']}/${data['image_path']}`">

    <div class="tooltip_content">
      <h1 class="title">{{ data['name'] }}</h1>
      <h1 class="description">{{ add_line_breaks(data['overview']) }}</h1>
    </div>

  </div>

</template>

<style scoped>
.tag_tooltip {
  position: absolute;
  overflow: hidden;
  /*background: linear-gradient(to left, #41404d 60%, #605c57 100%);*/

  box-shadow: 0 0 calc(v-bind(text_size) * 8px) rgba(0, 0, 0, 1);
  border-radius: calc(v-bind(text_size) * 50px);
  background-color: #2b2a34;

  z-index: 30;

  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  gap: calc(v-bind(text_size) * 10px);

  height: calc(v-bind(text_size) * 4em);

  opacity: 0;
  visibility: hidden;
  transition: 300ms;
}

.tag_tooltip:after {
  /*outline: 1px solid red;*/
  content: "";
  height: 100%;
  padding: 0 calc(v-bind(text_size) * 10px) 0 0;
}

.tooltip_content {
  display: flex;
  flex-flow: column nowrap;
  gap: calc(v-bind(text_size) * 7px);
  /*padding: calc(v-bind(text_size) * 10px) 0 calc(v-bind(text_size) * 10px) 0;*/
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
  white-space: pre;
}

.tag_preview {
  height: 100%;
  /*width: 100%;*/
  filter: drop-shadow(0 0 calc(v-bind(text_size) * 5px) rgba(0, 0, 0, 0.75));
}
</style>