<script setup>
import {defineProps, defineEmits, ref, watch, inject} from 'vue'

const props = defineProps(['rating', 'rating_desc'])

</script>

<template>

  <div class="rating_container">
    <div class="rating_content dark_accent">
      <h1 class="rating_title">{{ rating }}</h1>
      <h1 class="rating_desc"> {{ rating_desc[rating] }}</h1>
    </div>
  </div>

</template>

<script>
export default {
  name: "RatingHeader"
}
</script>
<style scoped>

.rating_container {
  /*outline: 1px blue solid;*/
  position: sticky;

  width: 100%;
  user-select: none;
  top: 20px;
  /*margin: 5px;*/
  z-index: 10;
}

.rating_content {
  /*outline: 1px blue solid;*/
  width: fit-content;

  display: flex;
  align-items: center;

  gap: 15px;

  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}

.dark_accent {
  box-shadow: 0 0 5px rgba(0, 0, 0, 1);
}

.rating_title {
  /*font-family: "Arial Black", serif;*/
  font-size: 1em;
}

.rating_title::after {
  /*display: block;*/
  content: "★";
  color: #1e8efd;
}

.rating_desc {
  /*font-family: Calibri, serif;*/
  font-size: 0.8em;
}
</style>