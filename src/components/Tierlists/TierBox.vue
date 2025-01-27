<script setup>
import {inject} from "vue";
import router from "@/router";

let props = defineProps(["b_width", "b_height", "box_data"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="tier_box" @click="router.push(box_data['link'])">

    <div class="top_content">
      <img :src="box_data['image']" alt="tier_list_box_image" class="bg_image">
    </div>

    <div class="box_content">
      <h1>{{ box_data['name'] }}</h1>
      <h3 v-if="box_data['desc']">{{ box_data['desc'] }}</h3>
    </div>

  </div>
</template>

<style scoped>
.tier_box {
  position: relative;
  display: flex;
  flex-flow: column;

  list-style: none;
  color: white;
  background-color: #2b2a34;
  text-decoration: none;
  cursor: pointer;

  border-radius: 10px;
  border: 0 solid #464646;

  filter: drop-shadow(5px 5px 6px black);
  transition: 50ms ease-in-out;
  clip-path: inset(0% 0% 0% 0% round 10px);
}

.box_content {
  padding: 6px 6px 10px 10px;
  display: flex;
  flex-flow: column;
  z-index: 10;
  background-color: #25222a;
  transition: 100ms ease-out;
}

.tier_box:hover .box_content {
  background-color: #36204a;
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

  color: rgba(255, 255, 255, 0.4);
}

.top_content {
  width: 100%;
  height: v-bind(b_height);

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
    .bg_image {
      opacity: 100%;
    }

    .vignette {
      height: 100%;
      width: auto;
      background: radial-gradient(circle at center, rgba(255, 255, 255, 0) 70%, rgba(0, 0, 0, 0.25) 100%);
    }

    .tier_box {
      width: 100%;
      clip-path: inset(0% 0% 0% 0% round 20px);
    }
  }
}
</style>
