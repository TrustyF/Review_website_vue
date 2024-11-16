<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["b_width", "b_height", "box_data"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

let loaded = ref(false)

</script>

<template>
  <RouterLink class="tier_box" :to="box_data['link']" v-show="loaded">
    <div class="tier_box_wrapper">

      <div class="top_content">
        <img :src="box_data['image']" @load="loaded=true" alt="tier_list_box_image" class="bg_image">
      </div>

      <div class="box_content">
        <h1>{{ box_data['name'] }}</h1>
        <h3 v-if="box_data['desc']">{{ box_data['desc'] }}</h3>
      </div>

    </div>

  </RouterLink>
</template>

<style scoped>
.tier_box {
  position: relative;

  list-style: none;
  color: white;
  text-decoration: none;

  width: v-bind(b_width);

  filter: drop-shadow(5px 5px 6px black);
  transition: 50ms ease-in-out;
}

.tier_box_wrapper {
  position: relative;
  display: flex;
  flex-flow: column;
  transition: 150ms ease-in-out;
}

.box_content {
  padding: 10px;
  margin-top: -10px;
  display: flex;
  flex-flow: column;

  gap: 5px;
  transition: 100ms ease-out;

  background-color: #25222a;
  border-radius: 10px;
}

.box_content h1 {
  font-size: 1.2em;
  line-height: normal;
  font-weight: 500;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

.box_content h3 {
  font-size: 0.7em;
  font-weight: 0;
  letter-spacing: 0.03em;

  color: rgba(255, 255, 255, 0.5);
}

.tier_box:hover .tier_box_wrapper {
  background-color: #36204a;
}

.bg_image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px 10px 0 0;

  -webkit-animation: fadein 0.5s; /* Safari, Chrome and Opera > 12.1 */
  -moz-animation: fadein 0.5s; /* Firefox < 16 */
  -ms-animation: fadein 0.5s; /* Internet Explorer */
  -o-animation: fadein 0.5s; /* Opera < 12.1 */
  animation: fadein 0.5s;
}

@media only screen and (max-width: 1000px) {
}
</style>