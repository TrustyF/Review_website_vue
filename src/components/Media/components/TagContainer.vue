<script setup>
import {defineProps,getCurrentInstance, defineEmits, toRefs, ref, watch, onMounted, onUnmounted, inject} from 'vue'
import FloatingVue from 'floating-vue'

const props = defineProps(['tag_input'])
const tag_path = "./assets/tags/icons/"
const forceVis = inject('forceVis')

const screenRect = ref(null)
const screenSide = ref(false)

let tagAmount = ref(0)

function calcScreenSide() {
  // let instance = getCurrentInstance()
  // console.log(instance.parent)
  // let parent = document.getElementById(instance.parent.uid)
  let rect = screenRect.value.getBoundingClientRect()
  let screen = [parent.outerWidth, parent.outerHeight]

  screenSide.value = rect.right > (screen[0] / 2);
}

function calcTagAmount() {
  if (props.tag_input !== undefined) {
    tagAmount.value = props.tag_input.length
  }
}

onMounted(() => {
  calcScreenSide()
  calcTagAmount()
  window.addEventListener('resize', calcScreenSide)
})


onUnmounted(() => {
  window.removeEventListener('resize', calcScreenSide)
})
</script>

<template>
  <div>
    <div ref="screenRect" class="tag_wrapper" >

      <div class="tooltip" v-for="tag in tag_input" :key="tag['name']">

        <img class="tag_icon" v-lazy="`${tag_path}${tag['tier']}/${tag['image']}`"
             :alt="tag['image']">

        <div :class="screenSide ?'hover_box_left' : 'hover_box' ">
          <div class="description">
            <p class=tag_name>{{ tag['name'] }}</p>
            <p class="tag_description">{{ tag['description'] }}</p>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>
<style scoped>

.tag_wrapper {
  display: flex;
  flex-flow: column;
  /*outline: red 1px solid;*/
  /*width: 200px;*/
  user-select: none;
  cursor: help;
  /*height: 300px;*/
  font-weight: normal;
}

.tag_preview {
  display: flex;
  flex-flow: column;
  /*outline: red 1px solid;*/
  /*width: 200px;*/
}

.hover_box {
  position: absolute;
  left: 0;
  top: 0;
  transform: translate(55px, 0);
  padding: 10px;
  border-radius: 5px;

  visibility: hidden;
  opacity: 0;

  color: black;
  background-color: white;
  transition: 100ms ease-in-out;

  filter: drop-shadow(0px 0 2px rgba(0, 0, 0, 1));
  -webkit-filter: drop-shadow(0px 0 2px rgba(0, 0, 0, 1));
  z-index: 99;
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
  color: black;
  background-color: white;
  padding: 10px;
  border-radius: 5px;

  visibility: hidden;
  opacity: 0;

  transition: 100ms ease-out;

  filter: drop-shadow(0px 0 2px rgba(0, 0, 0, 1));
  z-index: 99;
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

  /*visibility: hidden;*/
  /*opacity: 0;*/

  transition: ease-in-out 100ms;
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
  margin-bottom: 5px;
}

.tag_description {
  font-size: 1.2em;
  opacity: 0.6;
  line-height: 15px;
  max-width: 150px;
  /*outline: 1px solid red;*/
}

.tag_icon {
  padding: 5px;
  width: 40px;
  overflow: hidden;
}

.tag_gradient_wrapper {
  position: absolute;
  width: 200px;
  height: 300px;
  overflow: hidden;
  border-radius: 8px 0 0 0;
  pointer-events: none;
  /*outline: green solid 1px;*/

  visibility: hidden;
  opacity: 0;

  transition: ease-in-out 100ms;
}

.tag_wrapper:hover .tag_gradient_wrapper {
  visibility: visible;
  opacity: 100%;
}

.tag_gradient_background {
  /*outline: green solid 1px;*/
  overflow: hidden;
  width: 100px;
  position: absolute;
  transform: translate(-70%, -15%);
  background-color: rgba(0, 0, 0, 0.9);
  filter: blur(20px);
}

.one_tag {
  height: 50px;
}

.two_tag {
  height: 130px;
}

.three_tag {
  height: 190px;
}

</style>