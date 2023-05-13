<script setup>
import {defineProps, defineEmits, ref, watch, inject} from 'vue'

const devMode = inject('devMode')
const props = defineProps(['data'])

let overflowTitleLength = '-100%'

function calcTitleOverflow() {
  if (props.data['title'].length > 10) {
    overflowTitleLength = 100
  }
}

// calcTitleOverflow()

</script>

<template>
  <div class="content">
    <p class="title" v-if="data['title']">{{ data['title'] }}</p>
    <p class="date" v-if="data['release_date']">{{ data['release_date'].split("-")[0] }}</p>

    <div v-if="devMode">
      <!--      <span> -&#45;&#45; </span>-->
      <!--      <p class="date" v-if="data['images']">{{ data['images']['posters'].length }}</p>-->
      <!--      <p class="date" v-if="data['date_rated']">{{ data['date_rated'] }}</p>-->
    </div>
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
  overflow: hidden;

  margin: 5px 10px 10px 10px;
}

.title {
  /*outline: 1px solid red;*/
  font-size: 0.8em;
  text-align: left;
  margin: 0;
  white-space: nowrap;
  transition: linear;
}

.title:hover {
  transform: translate(v-bind('overflowTitleLength'));
  transition: linear 10s;
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