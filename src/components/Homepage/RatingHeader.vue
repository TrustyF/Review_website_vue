<script setup>
import {defineProps, defineEmits, ref, watch} from 'vue'

const props = defineProps(['rating','rating_desc'])

</script>

<template>
  <div class="rating_container">
    <div class="rating_content">
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
  width: 100%;
  user-select: none;
  position: sticky;
  top: 20px;
  /*margin: 5px;*/
  z-index: 10;
  /*outline: 1px red solid;*/
}

.rating_content {
  background-color: white;
  /*outline: 1px blue solid;*/

  width: fit-content;

  display: flex;
  justify-content: flex-start;
  align-items: center;
  flex-flow: row wrap;
  align-content: flex-start;

  gap: 15px;

  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}

.rating_title {
  /*font-family: "Arial Black", serif;*/
  font-size: 1em;
}
.rating_title::after {
  /*display: block;*/
  content: "★";
}

.rating_desc {
  /*font-family: Calibri, serif;*/
  font-size: 0.8em;
}
</style>