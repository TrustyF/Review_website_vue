<script setup>
import '@/styles/tag_container.css'
</script>

<template>
  <div class="tooltip">
    <PopperComp :hover="true" :arrow="true" placement="right">
      <img class="tag_icon" :src="tag['path']" :alt="tag['path']">
      <template #content>
        <img class="description_icon" :src="tag['path']" alt="desc_icon">
        <div class="description">
          <h3 class=tag_name>{{ tag['name'] }}</h3>
          <h1 class="tag_description">{{ tag['description'] }}</h1>
        </div>
      </template>
    </PopperComp>
  </div>
</template>

<script>
export default {
  name: "TagContainer",
  props: {
    tag: Object,
  },
  watch: {
    tag(n, o) {
      console.log(n, o)
    }
  }
}
</script>