<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import {BarChart, LineChart} from 'vue-chart-3';
import {Chart, registerables} from "chart.js";
import chartTrendline from 'chartjs-plugin-trendline';
import axios from "axios";

Chart.register(...registerables, chartTrendline);

let props = defineProps(["test"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

let stats = ref()
let stat_media_type = ref("movie")
let stat_media_type_colors = [
  '#DA073B',
  '#755800',
  '#004139',
  '#0D6A87',
  '#07475A',
  '#690d87',
]

function cleanArray(arr) {
  return arr.every(item => item === undefined) ? [] : arr;
}

let rating_stats = computed(() => {
  if (stats.value === undefined) {
    return {
      labels: [],
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
        cubicInterpolationMode: 'monotone',
      },
      {
        label: 'Public rating',
        data: Object.values(stats.value['public_ratings'][stat_media_type.value]),
        backgroundColor: [stat_media_type_colors[3]],
        borderColor: [stat_media_type_colors[3]],
        pointRadius: 3,
        cubicInterpolationMode: 'monotone',
      }],

  }
})
let date_stats = computed(() => {
  if (stats.value === undefined) {
    return {
      labels: [],
      datasets: [
        {
          data: [],
          backgroundColor: []
        }]
    }
  }

  let filtered_avg_rating = Object.values(stats.value['avg_rating_release_date'][stat_media_type.value]).map((e) => {
    if (e.length >= 1) return e.reduce((a, b) => a + b, 0) / e.length
    else return undefined
  })

  let filtered_avg_pub_rating = Object.values(stats.value['avg_pub_rating_release_date'][stat_media_type.value]).map((e) => {
    if (e.length >= 1) return (e.reduce((a, b) => a + b, 0) / e.length)
    else return undefined
  })

  let dates = Object.values(stats.value['release_dates'][stat_media_type.value]).map((e) => e.length)

  // check any values are left

  return {
    labels: Object.keys(stats.value['release_dates'][stat_media_type.value]),
    datasets: [
      {
        type: 'line',
        label: 'Average rating',
        data: !filtered_avg_rating.every(element => element === undefined) ? filtered_avg_rating : [],
        backgroundColor: [stat_media_type_colors[0]],
        borderColor: [stat_media_type_colors[0]],
        pointRadius: 0,
        cubicInterpolationMode: 'monotone',
        spanGaps: false,
        yAxisID: 'y1',
        trendlineLinear: {
          lineStyle: "dotted",
          width: 1
        }
      },
      {
        type: 'line',
        label: 'Average public rating',
        data: !filtered_avg_pub_rating.every(element => element === undefined) ? filtered_avg_pub_rating : [],
        backgroundColor: [stat_media_type_colors[3]],
        borderColor: [stat_media_type_colors[3]],
        pointRadius: 0,
        cubicInterpolationMode: 'monotone',
        spanGaps: false,
        yAxisID: 'y1',
        trendlineLinear: {
          lineStyle: "dotted",
          width: 1
        }
      },
      {
        type: 'bar',
        label: 'Release date',
        data: dates,
        backgroundColor: [stat_media_type_colors[1]],
        yAxisID: 'y',
        barPercentage: 1,
        categoryPercentage: 1,
      },

    ],
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

  let filtered_avg_runtime = Object.values(stats.value['avg_rating_runtimes'][stat_media_type.value]).map((e) => {
    if (e.length >= 10) return e.reduce((a, b) => a + b, 0) / e.length
    else return undefined
  })

  let filtered_avg_pub_runtime = Object.values(stats.value['avg_pub_rating_runtimes'][stat_media_type.value]).map((e) => {
    if (e.length >= 10) return (e.reduce((a, b) => a + b, 0) / e.length)
    else return undefined
  })

  return {
    labels: Object.keys(stats.value['runtimes'][stat_media_type.value]),
    datasets: [
      {
        type: 'line',
        label: 'Average rating',
        data: cleanArray(filtered_avg_runtime),
        backgroundColor: [stat_media_type_colors[0]],
        borderColor: [stat_media_type_colors[0]],
        pointRadius: 0,
        cubicInterpolationMode: 'monotone',
        spanGaps: true,
        yAxisID: 'y1',
        trendlineLinear: {
          lineStyle: "dotted",
          width: 1
        }
      },
      {
        type: 'line',
        label: 'Average public rating',
        data: cleanArray(filtered_avg_pub_runtime),
        backgroundColor: [stat_media_type_colors[3]],
        borderColor: [stat_media_type_colors[3]],
        pointRadius: 0,
        cubicInterpolationMode: 'monotone',
        spanGaps: true,
        yAxisID: 'y1',
        trendlineLinear: {
          lineStyle: "dotted",
          width: 1
        }
      },
      {
        label: 'Runtime (minutes)',
        data: Object.values(stats.value['runtimes'][stat_media_type.value]).map((e) => e.length),
        backgroundColor: [stat_media_type_colors[2]],
        barPercentage: 1,
        categoryPercentage: 1,
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
const release_date_stats_options = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      text: 'Release distribution',
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
    tooltip: {
      callbacks: {
        footer: ((elems) => {
          return stats.value['release_dates'][stat_media_type.value][elems[0].label].slice(0, 5)
        }),
      }
    }
  },
  scales: {
    x: {
      display: true,
    },
    y: {
      display: false,
      // min: 1,
      // max: 100,
    },
    y1: {
      display: true,
      position: 'right',
      min: 1,
      max: 10,
    }
  },

});
const runtime_stats_options = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      text: 'Runtime distribution',
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
    tooltip: {
      callbacks: {
        footer: ((elems) => {
          return stats.value['runtimes'][stat_media_type.value][elems[0].label].slice(0, 5)
        }),
      }
    }

  },
  scales: {
    x: {
      display: true,
    },
    y: {
      display: false,
      // min: 1,
      // max: 100,
    },
    y1: {
      display: true,
      position: 'right',
      min: 1,
      max: 10,
    }
  },


});

async function get_stats() {

  const url = new URL(`${curr_api}/media/get_stats`)

  let result = await axios(
      {
        method: 'GET',
        url: url,
      }).then(response => response.data)
      .catch(error => {
        console.log('get_stats', error.response)
        return []
      })
  stats.value = result
  // console.log(result)
  // console.log('result', Object.values(stats.value['avg_rating_release_date'][stat_media_type.value]).map((e) => {
  //   return (e.reduce((a, b) => a + b, 0))
  // }))
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
  // window.scrollTo(0, 20000)
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