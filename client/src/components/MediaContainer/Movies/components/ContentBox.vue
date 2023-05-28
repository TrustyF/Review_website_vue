<script setup>
import {defineProps, defineEmits, onMounted, ref, watch, inject} from 'vue'

const devMode = inject('devMode')
const darkMode = inject('darkMode')
const props = defineProps(['data'])

let overflowTitleLength = ref()
let overflowTitleSpeed = ref()
const titleRef = ref()

function calcTitleOverflow() {
  if (props.data['title'] === undefined) return

  let text_len = props.data['title'].length
  text_len += props.data['title'].split(" ").length
  const text_size = titleRef.value.clientWidth / text_len
  if (text_len > 36) {
    overflowTitleLength.value = `-${(text_len - 30) * (text_size * 1.2)}px`
    overflowTitleSpeed.value = `${((text_len - 30) * (text_size * 1.2)) / 50}s`
  }
}

onMounted(() => {
  calcTitleOverflow()
})

</script>

<template>
  <div class="content">
    <p class="title" ref="titleRef" v-if="data['title']">{{ data['title'] }}</p>
    <p class="date" v-if="data['release_date']">{{ data['release_date'].split("-")[0] }}</p>

    <!--    <div v-if="devMode">-->
    <!--      <p class="date" v-if="data['contentRating']">{{ data['contentRating'] }}</p>-->
    <!--      <p class="date" v-if="data['date_rated']">{{ data['date_rated'] }}</p>-->
    <!--    </div>-->

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
  margin: 5px 10px 5px 10px;
  overflow: hidden;
}

.title {
  /*outline: 1px solid red;*/
  font-size: 0.8em;
  font-weight: normal;
  text-align: left;
  margin: 0;
  white-space: nowrap;
  transition: linear;
  cursor: default;
}

.title:hover {
  transform: translate(v-bind('overflowTitleLength'));
  transition: linear v-bind('overflowTitleSpeed');
}

.date, .rating {
  /*outline: 1px solid red;*/

  font-size: 0.7em;
  text-align: left;
  margin: 0;
  opacity: 0.6;
  /*color: rgba(0, 0, 0, 0.6);*/

  /*overflow-wrap: normal;*/
}
</style>