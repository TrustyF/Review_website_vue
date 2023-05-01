<script setup>
import {defineProps, defineEmits, ref, watch} from 'vue'

const props = defineProps(['tag_input'])
const tag_path = "./assets/tags/icons/"
console.log('props', props['tag_input'])
</script>

<template>
  <div class="tag_wrapper">
    <div class="tooltip" v-for="tag in props['tag_input']" :key="tag['name']">
      <PopperComp :hover="true" :arrow="true" placement="right">
        <img class="tag_icon" :src="tag_path + tag['image']" :alt="tag['image']">
        <template #content>
          <div class="hover_box">
            <img class="description_icon" :src="tag_path + tag['image']" alt="desc_icon">
            <div class="description">
              <h3 class=tag_name>{{ tag['name'] }}</h3>
              <h1 class="tag_description">{{ tag['description'] }}</h1>
            </div>
          </div>
        </template>
      </PopperComp>
    </div>
  </div>
</template>

<script>
export default {
  name: "TagContainer"
}
</script>
<style scoped>
.tag_icon {
  padding: 5px;
  width: 40px;
  margin: 0;

  filter: drop-shadow(0px 0 3px rgba(255, 255, 255, 0.5))
}

.hover_box {
  background-color: white;
}

.tag_name {
  /*outline: 1px solid red;*/
  font-size: 1.4em;
  text-align: left;
  margin: 0;
  /*text-decoration: underline;*/
  /*overflow: hidden;*/
  white-space: nowrap;
  line-height: normal;
}

.tag_description {
  /*outline: 1px solid red;*/

  font-size: 1.2em;
  text-align: left;
  margin: 0;
  width: max-content;

  color: rgba(0, 0, 0, 0.6);

  overflow-wrap: break-word;
}

.tooltip {
  display: inline-block;
  position: relative;
  text-align: left;
  font-size: 0.7em;
}

</style>