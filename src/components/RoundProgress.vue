<script setup>
import '../styles/round_progress_bar.css'
</script>

<template>
  <PopperComp :hover="true" :arrow="true" placement="top" :append-to-body="true">
    <div class="gauge" :style="`width: 40px; --rotation:${data*18}deg;`">
      <div class="percentage"></div>
      <div class="mask"></div>
      <span class="value" v-if="number">{{ data }}</span>
    </div>
    <template #content>

    </template>
  </PopperComp>

</template>

<script>
export default {
  name: "RoundProgress",
  props: {
    data: Number,
    number: Boolean
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

.gauge {
  /*outline: 1px red solid;*/
  position: relative;
  border-radius: 50%/100% 100% 0 0;
  /*background: linear-gradient(to left, #c0392b 0%, #f1c40f 50%, #1abc9c 100%);*/
  background: linear-gradient(to right, #c0392b 0%, #f1c40f 50%, #1abc9c 100%);
  overflow: hidden;
}

.gauge:before {
  content: "";
  display: block;
  padding-top: 50%; /* ratio of 2:1*/
}

.gauge .chart {
  /*overflow: hidden;*/
}

.gauge .mask {
  position: absolute;
  left: 20%;
  right: 20%;
  bottom: 0;
  top: 40%;
  background-color: #fff;
  border-radius: 50%/100% 100% 0 0;
}

.gauge .percentage {
  position: absolute;
  top: -1px;
  left: -1px;
  bottom: 0;
  right: -1px;
  background-color: rgba(230, 230, 230, 1);
  transform: rotate(var(--rotation));
  transform-origin: bottom center;
}

.gauge .value {
  position: absolute;
  bottom: 0;
  left: 0;
  font-size: 0.6em;
  width: 100%;
  text-align: center;
}

.gauge .min {
  position: absolute;
  bottom: 0;
  left: 5%;
}

.gauge .max {
  position: absolute;
  bottom: 0;
  right: 5%;
}

.danger_tag_name {
  /*outline: 1px solid red;*/
  font-size: 1em;
  text-align: left;
  margin: 0;
  /*text-decoration: underline;*/
  /*overflow: hidden;*/
  white-space: nowrap;
  line-height: normal;
}

.danger_tag_description {
  /*outline: 1px solid red;*/

  font-size: 0.8em;
  text-align: left;
  margin: 0;
  width: max-content;

  color: rgba(0, 0, 0, 0.6);

  overflow-wrap: break-word;
}
</style>