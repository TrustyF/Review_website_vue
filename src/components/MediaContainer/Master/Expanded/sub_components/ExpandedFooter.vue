<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["data"]);
const curr_api = inject("curr_api");

</script>

<template>
  <div class="footer_wrapper">
    test
  </div>
</template>

<style scoped>
.footer_wrapper {
  outline: 1px solid blue;
  /*margin: 30px 30px 0 30px;*/
  display: flex;
  /*height: 50%;*/
}
.poster {
  object-fit: cover;
}

</style>