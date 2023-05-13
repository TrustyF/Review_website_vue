<script setup>
import {defineProps, defineEmits, ref, watch} from 'vue'
import FloatingVue from 'floating-vue'

const props = defineProps(['tag_input', 'screen_side'])
const tag_path = "./assets/tags/icons/"
</script>

<template>
  <div class="tag_wrapper">
    <div class="tooltip" v-for="tag in tag_input" :key="tag['name']">
      <img :class="'tag_icon ' + `${tag['tier']}_glow`" :src="`${tag_path}${tag['tier']}/${tag['image']}`" :alt="tag['image']">
      <div :class="props['screen_side'] ? 'hover_box_left' : 'hover_box'">
        <div class="description">
          <p class=tag_name>{{ tag['name'] }}</p>
          <p class="tag_description">{{ tag['description'] }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TagContainer"
}
</script>
<style scoped>

.tag_wrapper {
  display: flex;
  flex-flow: column;
  /*outline: green solid 1px;*/
  /*min-width: 200px;*/
}

.hover_box {
  position: absolute;
  left: 0;
  top: 0;
  transform: translate(55px, 0);
  background-color: white;
  padding: 10px;
  border-radius: 5px;

  visibility: hidden;
  opacity: 0;

  transition: 0.1s ease-in-out;
  filter: drop-shadow(0px 0 2px rgba(0, 0, 0, 1));
  z-index: 400000;
}

.hover_box:after {
  content: '';
  position: absolute;
  top: 0;
  left: -5px;
  margin: 10px auto;
  /*width: 0;*/
  /*height: 0;*/
  border-right: 15px solid white;
  border-top: 15px solid transparent;
  border-bottom: 15px solid transparent;
}

.hover_box_left {
  position: absolute;
  right: 0;
  top: 0;
  transform: translate(-205px, 0);
  background-color: white;
  padding: 10px;
  border-radius: 5px;

  visibility: hidden;
  opacity: 0;

  transition: 0.1s ease-in-out;
  filter: drop-shadow(0px 0 2px rgba(0, 0, 0, 1));
  z-index: 400000;
}

.hover_box_left:after {
  content: '';
  position: absolute;
  top: 0;
  right: -5px;
  margin: 10px auto;
  /*width: 0;*/
  /*height: 0;*/
  border-left: 15px solid white;
  border-top: 15px solid transparent;
  border-bottom: 15px solid transparent;
}

.tooltip {
  /*display: inline-block;*/
  /*outline: 1px purple solid;*/
  position: relative;
  text-align: left;
  font-size: 0.7em;
  width: 200px;
}

.tag_icon:hover + .hover_box {
  visibility: visible;
  opacity: 100%;
}
.tag_icon:hover + .hover_box_left {
  visibility: visible;
  opacity: 100%;
}

.visible_override {
  visibility: visible;
  opacity: 100%;
}

.description {
  display: inline-block;
  position: relative;
  /*outline: 1px solid blue;*/
  max-width: 200px;
  text-overflow: ellipsis;
}

.tag_name {
  font-size: 1.4em;
  text-align: left;
}

.tag_description {
  font-size: 1.2em;
  color: rgba(0, 0, 0, 0.6);
}

.tag_icon {
  padding: 5px;
  width: 40px;
  /*filter: drop-shadow(0px 0 2px rgba(0, 0, 0, 1)) drop-shadow(0px 0 4px rgba(0, 0, 0, 1))*/
}
.gold_glow {
  filter: drop-shadow(0px 0 4px #f6df86)
}
.green_glow {
  filter: drop-shadow(0px 0 4px #aace9f)
}
.purple_glow {
  filter: drop-shadow(0px 0 4px #C58CC0FF)
}
.red_glow {
  filter: drop-shadow(0px 0 4px #ff74a1)
}
.silver_glow {
  filter: drop-shadow(0px 0 4px #a6caf8)
}

</style>