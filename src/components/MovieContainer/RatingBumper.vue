<script setup>
import {defineProps, defineEmits, ref, watch} from 'vue'

const props = defineProps(['rating', 'user_rating'])
const user_rating = Math.round( props['user_rating'] * 10) / 10

</script>

<template>
  <div>
    <p class="rating">{{ props['rating'] }} </p>
    <p class="user_rating">{{ user_rating }} </p>
  </div>
</template>

<script>
export default {
  name: "RatingBumper"
}
</script>
<style scoped>
.rating {
  width: min-content;
  background-color: rgba(1,1,1,0.75);
  color: white;

  font-size: 0.7em;
  padding: 5px 5px 5px 5px;
  border-radius: 0 10px 10px 0;
}
.rating::after {
  content: "★";
  color: dodgerblue;
}
.user_rating {
  width: min-content;
  background-color: rgba(1,1,1,0.75);
  color: white;

  transform: translate(0, 3px);

  font-size: 0.7em;
  padding: 5px 5px 5px 5px;
  border-radius: 0 10px 10px 0;
}
.user_rating::after {
  content: "★";
  color: gold;
}
</style>