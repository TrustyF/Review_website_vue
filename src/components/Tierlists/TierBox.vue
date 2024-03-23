<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["b_width", "b_height", "box_data"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

let loaded = ref(false)

</script>

<template>
  <RouterLink class="tier_box" :to="box_data['link']" v-show="loaded">
    <div class="tier_box_wrapper" >
      <div class="box_content">
        <h1>{{ box_data['name'] }}</h1>
      </div>

      <div class="box_gradient"></div>
      <div class="vignette"></div>
      <img :src="box_data['image']" @load="loaded=true" alt="tier_list_box_image" class="bg_image">
    </div>
  </RouterLink>
</template>

<style scoped>
.tier_box {
  position: relative;
  /*outline: 1px solid orange;*/

  list-style: none;
  color: white;
  text-decoration: none;

  height: v-bind(b_height);
  width: v-bind(b_width);
  border-radius: 10px;
  outline: 0 solid #969696;

  filter: drop-shadow(5px 5px 6px black);
  transition: 50ms ease-in-out;
}

.tier_box_wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;

  border: 0 solid #464646;
  /*outline: 1px solid red;*/

  height: 100%;
  width: 100%;

  background-color: #2b2a34;
  transition: 150ms ease-in-out;
  clip-path: inset(0% 0% 0% 0% round 10px);
}

.box_content {
  font-weight: 1000;
  line-height: 1.2em;

  margin-top: auto;

  font-size: 1.5em;
  text-align: center;
  width: 100%;
  padding: 20px;
  z-index: 20;

  /*background-color: #1c1b23;*/
  /*background-color: rgba(28, 27, 35, 0.8);*/
  filter: drop-shadow(0 0 3px black) drop-shadow(0 0 2px black);
}

.box_gradient {
  position: absolute;
  height: 100%;
  width: 100%;
  z-index: 10;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 50%, rgba(0, 0, 0, 0.9) 100%);

  transition: 150ms ease-in-out;
}

.vignette {
  position: absolute;
  width: 100%;
  aspect-ratio: 1;
  z-index: 11;
  background: radial-gradient(circle at center, rgba(255, 255, 255, 0) 80%, rgba(0, 0, 0, 1) 110%);
  opacity: 100%;
  transition: 150ms ease-in-out;
}

.bg_image {
  position: absolute;

  width: 100%;
  height: 100%;
  object-fit: cover;

  -webkit-animation: fadein 0.5s; /* Safari, Chrome and Opera > 12.1 */
  -moz-animation: fadein 0.5s; /* Firefox < 16 */
  -ms-animation: fadein 0.5s; /* Internet Explorer */
  -o-animation: fadein 0.5s; /* Opera < 12.1 */
  animation: fadein 0.5s;
  /*z-index: -1;*/
  /*opacity: 85%;*/
  transition: 150ms ease-in-out;
}

.tier_box:hover .bg_image {
  transform: scale(1.05);
  opacity: 100%;
}

.tier_box:hover .vignette {
  opacity: 0;
}
.tier_box:hover {
  outline: 0.1em solid #464646;
}


@media only screen and (max-width: 1000px) {
  .bg_image {
    opacity: 100%;
  }
  .vignette {
    height: 100%;
    width: auto;
    background: radial-gradient(circle at center, rgba(255, 255, 255, 0) 50%, rgba(0, 0, 0, 0.5) 100%);
  }
  .tier_box {
    width: 100%;
    clip-path: inset(0% 0% 0% 0% round 20px);
  }
}
</style>