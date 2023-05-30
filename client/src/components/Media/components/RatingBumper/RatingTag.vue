<script setup>
import {defineProps, defineEmits, ref, watch, onMounted, onUnmounted, computed, inject} from 'vue'

const props = defineProps(['image', 'name', 'desc', 'sub_desc', 'number', 'rating'])
const darkMode = inject('darkMode')

</script>

<template>
  <div class="tooltip">

    <div :class="darkMode ? 'box dark_accent' : 'box white'" v-if="rating">
      <h1 class="rating">{{ rating }}</h1>
      <img class="rating icon" v-if="image" v-lazy="image">
    </div>

    <div :class="darkMode ? 'box dark_accent' : 'box white'" v-if="!rating && !number">
      <h1 class="rating">{{ rating }}</h1>
      <img class="rating icon" v-if="image" v-lazy="image">
    </div>

    <div :class="darkMode ? 'box dark_accent' : 'box white'" v-if="number">
      <h1 class="rating"> {{ number }}</h1>
      <img class="rating icon" style="padding-left: 2px" v-lazy="image">
    </div>


    <div class="hover_box">
      <div class="description">
        <h1 class="tag_name">{{ name }}</h1>
        <h1 class="tag_description">{{ desc }}</h1>
        <h1 class="tag_description" style="font-size: 0.6em;margin-top: 5px;  color: rgba(0, 0, 0, 0.4);">
          {{ sub_desc }}</h1>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RatingTag"
}
</script>
<style scoped>
.box {
  filter: drop-shadow(0 0 2px rgba(0, 0, 0, 0.8));
  padding: 3px;
  border-radius: 5px;
  /*border: solid darkgrey 1px;*/
  display: flex;
  flex-flow: row;
  /*outline: 1px green solid;*/

  justify-content: center;
  justify-items: center;
  align-items: center;
  align-content: center;
}

.white {
  background-color: white;
}

.rating {
  font-size: 0.8em;
  line-height: normal;
  /*transform-origin: 0 0;*/
  /*margin-bottom: -50%;*/
  /*outline: 1px red solid;*/
}

.icon {
  /*padding-left: 3px;*/
  height: 15px;
  /*outline: 1px red solid;*/
}

.hover_box {
  position: absolute;
  left: 50%;
  top: -50%;
  transform: translate(-50%, -100%);

  font-weight: normal;
  color: black;
  background-color: white;
  padding: 10px;
  border-radius: 5px;
  filter: drop-shadow(0px 0 2px rgba(0, 0, 0, 0.5));

  /*outline: 2px red solid;*/
  visibility: hidden;
  opacity: 0;
  transition: 100ms ease-out;
}

.hover_box:after {
  content: '';
  position: absolute;
  display: inline-block;
  left: 0;
  right: 0;
  margin: 10px auto;
  width: 0;
  height: 0;
  border-top: 5px solid white;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
}

.tooltip:hover .hover_box {
  visibility: visible;
  opacity: 100%;
}

.tooltip {
  display: inline-block;
  position: relative;
  text-align: left;
  /*outline: 1px solid red;*/
}


.tag_name {
  font-size: 0.9em;
  margin-bottom: 5px;
  /*text-decoration: underline;*/
}

.tag_description {
  /*outline: 1px solid red;*/
  font-size: 0.7em;
  text-align: left;
  margin: 0;
  width: 200px;
  color: rgba(0, 0, 0, 0.6);
  overflow-wrap: break-word;
}

</style>