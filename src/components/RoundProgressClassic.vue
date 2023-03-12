<template>
  <div class="gauge_classic" :style="`--rotation:${(data/10 * 360)}deg;`">
    <div class="percentage_classic"></div>
    <div class="mask"></div>
    <span class="value_classic" v-if="number">{{ data }}</span>
  </div>
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
.gauge_classic {
  width: 50px;
  height: 50px;
  background: #fefcff;
  border-radius: 50%;
  border: 1px solid #cdcbd0;
}
</style>