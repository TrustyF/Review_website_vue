<script setup>
import '../styles/progress_bar.css'
</script>

<template>
  <PopperComp :hover="true" :arrow="true" placement="top" :append-to-body="false">
    <div class="container">
      <div v-for="elem in Array(data)" :key="elem" class="block"></div>
    </div>
    <template #content>

      <div v-if="data === 1">
        <h3 class=tag_name>Fast and furious tier</h3>
        <h1 class="tag_description">Easily digested and doesn't challenge the audience</h1>
      </div>

      <div v-if="data === 2">
        <h3 class=tag_name>Regular</h3>
        <h1 class="tag_description">Respects the audience and should be accessible to everyone</h1>
      </div>

      <div v-if="data === 3">
        <h3 class=tag_name>Challenging</h3>
        <h1 class="tag_description">Unconventional and will require your full attention</h1>
      </div>

      <div v-if="data === 4">
        <h3 class=tag_name>Experimental</h3>
        <h1 class="tag_description">Very difficult, reserved for the highest of movie snobs</h1>
      </div>

    </template>
  </PopperComp>

</template>

<script>
export default {
  name: "ProgressBar",
  props: {
    data: Number
  },
  watch: {
    data(n, o) {
      // console.log("progress bar", n, o)
    }
  }
}
</script>

<style>
:root {
  --popper-theme-background-color: white;
  /*--popper-theme-background-color-hover: #333333;*/
  /*--popper-theme-text-color: #ffffff;*/
  --popper-theme-border-width: 0px;
  --popper-theme-border-style: solid;
  --popper-theme-border-radius: 6px;
  --popper-theme-padding: 10px;
  --popper-theme-box-shadow: 0 2px 8px rgba(0, 0, 0, 0.75);
}
</style>