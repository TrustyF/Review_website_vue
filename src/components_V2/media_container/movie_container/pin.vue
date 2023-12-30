<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["data", "min_size"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

const tag_container = ref()
const tooltip_container = ref()


function compute_tag_position() {
  let tag = tag_container.value
  let tip = tooltip_container.value

  let tag_box = tag.getBoundingClientRect()
  let tip_box = tip.getBoundingClientRect()

  tip.style.top = `${(-tip_box.height - 10)}px`


  if (tag_box.x < (window.innerWidth / 2)) {
    tip.style.transform = 'translate(-25px,0)';
  } else {
    tip.classList.add('tag_tooltip_reversed')
    tip.style.transform = `translate(${-tip_box.width - 10}px,0)`;
  }


}

onMounted(() => {
  compute_tag_position()
})
</script>

<template>
  <div class="tag_box">
    <img ref="tag_container" class="tag_image" v-lazy="`public/tags/icons/${data['tier']}/${data['image_path']}`">

    <div ref="tooltip_container" class="tag_tooltip">
      <img class="tag_preview" v-lazy="`public/tags/icons/${data['tier']}/${data['image_path']}`">
      <div class="tooltip_content">
        <h1 class="title">{{ data['name'] }}</h1>
        <h1 class="description">{{ data['overview'] }}</h1>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tag_tooltip {
  position: absolute;
  background-color: #2b2a34;
  /*background: linear-gradient(to left, #41404d 60%, #605c57 100%);*/

  box-shadow: 1px 1px 8px rgba(0, 0, 0, 1), inset 0px 0px 3px #ececec;
  border-radius: 50px;

  padding: 10px 30px 10px 10px;
  max-width: 300px;
  z-index: 30;

  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  /*gap: 10px;*/
  opacity: 0;
  visibility: hidden;
  transition: 300ms ;
}
.tag_box:hover .tag_tooltip {
  opacity: 100%;
  visibility: visible;
  transition: 50ms ;
}
.tag_tooltip_reversed {
  flex-flow: row-reverse nowrap;
  padding: 10px 10px 10px 30px;
  /*border-radius: 15px 50px 50px 15px;*/
}



.tooltip_content {
  /*padding: 10px;*/
  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
  gap: 2px;
  padding: 10px;
}

.title {
  font-size: 1em;
  font-weight: 700;
  /*color: black;*/
  text-shadow: 1px 1px 3px black, 0 0 5px black;
}

.description {
  font-size: 0.8em;
  color: #b0b0b0;
  width: 200px;
  line-height: normal;
  text-shadow: 0 0 7px black;

}

.tag_preview {
  height: 70px;
  filter: drop-shadow(0 0 5px rgba(0, 0, 0, 0.75));
}

.tag_box {
  width: calc(v-bind(min_size) * 0.2px);
  height: calc(v-bind(min_size) * 0.2px);
}

.tag_image {
  width: 100%;
  height: 100%;
}
</style>