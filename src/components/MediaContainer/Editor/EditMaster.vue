<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import MediaExpanded from "@/components/MediaContainer/Expanded/Base/MediaExpanded.vue";
import MediaMaster from "@/components/MediaContainer/Master/Base/MediaMaster.vue";

let props = defineProps(["test"]);
const curr_api = inject("curr_api");
const edit_media = inject("edit_media");

</script>

<template>

  <div class="edit_master_wrapper">
    <div class="poster_pane">
      <div class="preview">
        <media-master :data="edit_media"></media-master>
      </div>
    </div>

    <div class="details_pane">
      <div v-for="(val,key) in edit_media" :key="key" style="display: flex;flex-flow: column wrap">
        <label :for="key">{{ key }}</label>
        <input :id="key" :type="typeof val" :value="val"
               @change="edit_media[key] = $event.target._value">
      </div>
    </div>
  </div>

</template>

<style scoped>
.edit_master_wrapper {
  background-color: #131215;
  position: relative;
  z-index: 50;

}

.poster_pane {
  outline: 1px solid red;
  height: 100%;
  width: 150px;
  display: flex;
  flex-flow: column wrap;
}

.details_pane {
  outline: 1px solid red;
  display: flex;
  flex-flow: row wrap;
  gap: 5px;
  /*width: 600px;*/
}
</style>