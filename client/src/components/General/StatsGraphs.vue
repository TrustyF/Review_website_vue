<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import {BarChart, LineChart} from 'vue-chart-3';
import {Chart, registerables} from "chart.js";
import axios from "axios";

Chart.register(...registerables);

let props = defineProps(["test"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

let stats = ref()
let stat_media_type = ref("movie")
let stat_media_type_colors = [
  '#DA073B',
  '#DAA507',
  '#8EC7D2',
  '#0D6A87',
  '#07475A',
  '#690d87',
]

let rating_stats = computed(() => {
  if (stats.value === undefined) {
    return {
      labels: [...Array(11).keys()],
      datasets: [
        {
          data: [],
          backgroundColor: []
        }]
    }
  }
  return {
    labels: Object.keys(stats.value['ratings'][stat_media_type.value]),
    datasets: [
      {
        label: 'My rating',
        data: Object.values(stats.value['ratings'][stat_media_type.value]),
        backgroundColor: [stat_media_type_colors[0]],
        borderColor: [stat_media_type_colors[0]],
        pointRadius: 3,
        // barPercentage: 1,
        // categoryPercentage: 0.7,
        // yAxisID: 'y',
        cubicInterpolationMode: 'monotone',
      },
      {
        label: 'Public rating',
        data: Object.values(stats.value['public_ratings'][stat_media_type.value]),
        backgroundColor: [stat_media_type_colors[3]],
        borderColor: [stat_media_type_colors[3]],
        pointRadius: 3,
        // barPercentage: 1,
        // categoryPercentage: 0.7,
        // yAxisID: 'y1',
        cubicInterpolationMode: 'monotone',
      }],

  }
})
let pub_rating_stats = computed(() => {
  if (stats.value === undefined) {
    return {
      labels: [...Array(11).keys()],
      datasets: [
        {
          data: [],
          backgroundColor: []
        }]
    }
  }
  return {
    labels: Object.keys(stats.value['public_ratings'][stat_media_type.value]),
    datasets: [{
      data: Object.values(stats.value['public_ratings'][stat_media_type.value]),
      backgroundColor: [stat_media_type_colors[3]],
    }],

  }
})
let date_stats = computed(() => {
  if (stats.value === undefined) {
    return {
      labels: [1900, 2024],
      datasets: [
        {
          data: [],
          backgroundColor: []
        }]
    }
  }
  return {
    labels: Object.keys(stats.value['release_dates'][stat_media_type.value]),
    datasets: [
      {
        data: Object.values(stats.value['release_dates'][stat_media_type.value]),
        backgroundColor: [stat_media_type_colors[1]],
      }],
  }
})
let runtime_stats = computed(() => {
  if (stats.value === undefined) {
    return {
      labels: [0, 250],
      datasets: [
        {
          data: [],
          backgroundColor: []
        }]
    }
  }
  return {
    labels: Object.keys(stats.value['runtimes'][stat_media_type.value]),
    datasets: [{
      data: Object.values(stats.value['runtimes'][stat_media_type.value]),
      backgroundColor: [stat_media_type_colors[2]],
    }],

  }
})

let total_media_count = computed(() => {
  if (stats.value === undefined) return 0
  return Object.values(stats.value['ratings'][stat_media_type.value]).reduce((partialSum, a) => partialSum + a, 0);
})
const rating_stats_options = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      text: 'Rating distribution',
      // position:'top',
      font: {
        weight: 'normal',
        color: 'white',
      }
    },
    legend: {
      position: 'top',
      display: true,
      labels: {
        color: "white",
      },
    },
  },
  scales: {
    x: {
      display: true,
    },
    y: {
      display: false,
      position: 'left',
    },
    y1: {
      display: false,
      position: 'right',
    },
  },

});
const pub_rating_stats_options = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      position: 'bottom',
      text: 'Public rating distribution',
      font: {
        weight: 'normal'
      }
    },
    legend: {
      position: 'top',
      display: false,
    },
  },
  scales: {
    x: {
      display: true,
    },
    y: {
      display: false,
    }
  },

});
const release_date_stats_options = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      position: 'bottom',
      text: 'Release year distribution',
      font: {
        weight: 'normal'
      }
    },
    legend: {
      position: 'top',
      display: false,
    },
  },
  scales: {
    x: {
      display: true,
    },
    y: {
      display: false,
    }
  },

});
const runtime_stats_options = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      position: 'bottom',
      text: 'Runtime distribution ( minutes )',
      font: {
        weight: 'normal'
      }
    },
    legend: {
      position: 'top',
      display: false,
    },
  },
  scales: {
    x: {
      display: true,
    },
    y: {
      display: false,
    }
  },

});

async function get_stats() {

  const url = new URL(`${curr_api}/media/get_stats`)

  stats.value = await axios(
      {
        method: 'GET',
        url: url,
      }).then(response => response.data)
      .catch(error => {
        console.log('get_stats', error.response)
        return []
      })
}

function switch_media(event) {
  let buttons = document.getElementsByClassName('graph_nav_button')
  Array.from(buttons).forEach((elem) => {
    elem.classList.remove('selected')
  })

  event.target.classList.add('selected')
  stat_media_type.value = event.target.textContent
}

onMounted(() => {
  get_stats()
})
</script>

<template>
  <div class="graphs_wrapper">


    <div class="sticky sticky_nav">
      <div class="graphs_count">
        <h1 class="graph_count_label">{{ total_media_count }} entries</h1>
      </div>
      <div class="graph_nav">
        <h1 :class="media !== stat_media_type ? 'graph_nav_button':'graph_nav_button selected'" @click="switch_media"
            v-for="media in ['movie','tv','youtube','manga','game']" :key="media">{{ media }}</h1>
      </div>
    </div>

    <div class="chart">
      <line-chart :chartData="rating_stats" :options="rating_stats_options"></line-chart>
    </div>
    <div class="chart">
      <bar-chart :chartData="date_stats" :options="release_date_stats_options"></bar-chart>
    </div>
    <div class="chart">
      <bar-chart :chartData="runtime_stats" :options="runtime_stats_options"></bar-chart>
    </div>


  </div>
</template>

<style scoped>
.graphs_wrapper {
  /*margin: auto;*/
  position: relative;
  /*outline: 1px solid orange;*/
  display: flex;
  flex-flow: column;
  gap: 20px;
}

.sticky {
  /*outline: 1px solid purple;*/
  position: sticky;
  top: 0;
  height: 0;
  z-index: 100;

  transition: top 250ms;
  transition-delay: 250ms;
}

.graph_nav {
  /*outline: 1px solid red;*/
  position: relative;
  /*top: 30px;*/
  display: flex;
  flex-flow: column;
  align-items: flex-start;
  gap: 10px;
  /*padding: 10px;*/
}

.chart {
  /*outline: 1px solid red;*/
  /*position: relative;*/
  /*height: 100%;*/
  /*max-height: 200px;*/
}

.graphs_count {
  position: absolute;
  display: flex;
  right: 0;
  padding: 10px;
  font-size: 0.8em;
  color: #969696;
  background-color: #1c1b23;
  border-radius: 5px;
}

.graph_nav_button {
  font-size: 0.8em;
  padding: 7px 10px 7px 10px;
  border: 2px solid #464646;
  border-radius: 8px;
  cursor: pointer;
  background-color: #1c1b23;
}

.selected {
  border: 2px solid #969696;
}
</style>