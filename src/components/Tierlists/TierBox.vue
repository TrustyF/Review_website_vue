<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["box_size", "box_data"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

let box_scale = 0.45
let tier_box_height = computed(() => props['box_size'][1] * box_scale + 'px')
let tier_box_width = computed(() => props['box_size'][0] * box_scale + 'px')

</script>

<template>
    <RouterLink class="tier_box" :to="box_data['link']">
      <div class="tier_box_wrapper">
        <div class="box_content">
          <h1>{{ box_data['name'] }}</h1>
        </div>

        <div class="box_gradient"></div>
        <img :src="box_data['image']" alt="tier_list_box_image" class="bg_image">
      </div>
    </RouterLink>
</template>

<style scoped>
.tier_box {
  outline: 1px solid orange;

  list-style: none;
  color: white;
  text-decoration: none;

  height: v-bind(tier_box_height);
  width: v-bind(tier_box_width);

  clip-path: inset(0% 0% 0% 0% round 5%);
}

.tier_box_wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;

  height: 100%;
  width: 100%;

  background-color: #2b2a34;
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
}
.bg_image {
  position: absolute;

  width: 100%;
  height: auto;
  object-fit: contain;

  z-index: 1;

  opacity: 50%;

  transition: 150ms ease-in-out;
}

.tier_box:hover .bg_image {
  transform: scale(1.05);
  opacity: 100%;
}

@media only screen and (max-width: 724px) {
  .tier_box{
    width: 100%;
    height: 300px;
    clip-path: inset(0% 0% 0% 0% round 20px);
  }
}
</style>