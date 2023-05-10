<script setup>
import {defineProps, defineEmits, ref, watch} from 'vue'

const props = defineProps(['data'])
</script>

<template>
  <div class="content">
    <p class="title" v-if="data['title']">{{ data['title'] }}</p>
<!--    <p class="title" v-if="data['original_title']">{{ data['original_title'] }}</p>-->
<!--    <p class="title" v-if="data['original_name']">{{ data['original_name'] }}</p>-->
    <p class="date" v-if="data['release_date']">{{ data['release_date'].split("-")[0] }}</p>
<!--    <p class="date" v-if="data['region']">{{ data['region'] }}</p>-->
<!--    <p class="rating">{{ data['my_rating'] + "★" }} </p>-->
  </div>

</template>

<script>
export default {
  name: "ContentBox"
}
</script>
<style scoped>
.content {
  /*user-select: none;*/
  /*outline: 1px solid red;*/
  display: grid;
  justify-content: space-between;
  flex-direction: column;

  margin: 5px 10px 10px 10px;
}

.title {
  /*outline: 1px solid red;*/
  font-size: 0.8em;
  text-align: left;
  margin: 0;
  /*overflow: hidden;*/
  /*white-space: pre-wrap;*/
}

.date, .rating {
  /*outline: 1px solid red;*/

  font-size: 0.7em;
  text-align: left;
  margin: 0;

  color: rgba(0, 0, 0, 0.6);

  /*overflow-wrap: normal;*/
}
</style>