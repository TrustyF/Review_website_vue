<script setup>
import {computed, inject, onMounted, ref} from "vue";
import {BarChart} from 'vue-chart-3';
import {Chart, registerables} from "chart.js";

import rating_info from '/home_images/rating_info.jpg'
import search_info from '/home_images/search_info.jpg'

Chart.register(...registerables);

const curr_api = inject("curr_api");

let stats = ref()
let stat_media_type = ref("movie")
let stat_media_type_colors = [
  '#DA073B',
  '#DAA507',
  '#8EC7D2',
  '#0D6A87',
  '#07475A',
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
    datasets: [{
      data: Object.values(stats.value['ratings'][stat_media_type.value]),
      backgroundColor: [stat_media_type_colors[0]],
    }],

  }
})
let total_media_count = computed(() => {
  if (stats.value === undefined) return 0
  return Object.values(stats.value['ratings'][stat_media_type.value]).reduce((partialSum, a) => partialSum + a, 0);
})
const options = ref({
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
      display: false,
    },
  },
  layout: {
    padding: {
      top: 40
    }
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

  const result = await fetch(url).then(response => response.json())
  console.log('result', result)
  stats.value = result

}

function switch_media(event) {
  console.log(event.target.textContent)

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
  <div class="home_wrapper">

    <div class="intro_text">
      <h2>Welcome to Trusty's Corner!</h2>
      <p>This was made for fun while learning web-dev. The goal was to more easily share my media recommendations with
        people and for my own love of cataloguing</p>
    </div>

    <div class="intro_text">
      <h1>Ratings</h1>
      <p>Ratings are split into 3 components: my rating, the public rating and the combined circle</p>
      <p> - The circle is meant to inform you at a glance of the approximate quality of said media</p>
      <img :src="rating_info" alt="rating_info" class="home_image">
    </div>

    <div class="intro_text">
      <h1>Searching</h1>
      <p>The search bar can search for many different fields including:<br>
        - approximate name<br>
        - genre<br>
        - tags<br>
        - studio<br>
        - author
      </p>
      <p>Filters can also be found next to the search bar and are applied additively</p>
      <img :src="search_info" alt="search_info" class="home_image">
    </div>

    <span style="height: 50px"></span>

    <div class="intro_text">
      <h1>Stats for nerds (me)</h1>
      <p>Rating distribution per media</p>
    </div>
    <div class="graphs_wrapper">
      <div class="graph_nav">
        <h1 :class="media !== stat_media_type ? 'graph_nav_button':'graph_nav_button selected'" @click="switch_media"
            v-for="media in ['movie','tv','youtube','manga','game']" :key="media">{{ media }}</h1>
      </div>

      <div class="graphs_count">
        <h1 class="graph_count_label">{{ total_media_count }} entries</h1>
      </div>

      <bar-chart :chartData="rating_stats" :options="options"></bar-chart>

    </div>
  </div>
</template>

<style scoped>
.home_wrapper {
  display: flex;
  flex-flow: column;
  gap: 20px;
  margin: 0 auto 0 auto;
  padding: 120px 150px 100px 150px;
  position: relative;
  /*outline: 1px solid red;*/
  min-height: 80vh;
  /*background-color: #1c1b23;*/
}

.intro_text {
  display: flex;
  flex-flow: column;
  gap: 10px;
  /*outline: 1px solid grey;*/
}

.intro_text h2 {
  font-size: 2em;
  font-weight: 1000;
}

.intro_text h1 {
  font-size: 1.5em;
  /*text-decoration: underline;*/
  font-weight: 800;
}

.intro_text p {
  font-size: 0.8em;
  font-weight: 100;
  line-height: 1.5em;
  color: #b0b0b0;
  /*margin-left: 20px;*/
}
.home_image {
  /*outline: 1px solid red;*/
  /*height: 200px;*/
  object-fit: contain;
  /*border: inset 5px #b0b0b0;*/
  clip-path: inset(0% 0% 0% 0% round 20px);
}

.graphs_wrapper {
  /*margin: auto;*/
  position: relative;
  /*outline: 1px solid orange;*/
  display: flex;
  flex-flow: column;
  gap: 20px;
}

.graph_nav {
  /*outline: 1px solid red;*/
  position: absolute;
  display: flex;
  flex-flow: column;
  align-items: flex-start;
  gap: 10px;
  z-index: 10;
  /*padding: 10px;*/
}

.graphs_count {
  position: absolute;
  display: flex;
  right: 0;
  /*padding: 10px;*/
  font-size: 0.8em;
  color: #969696;
}

.graph_nav_button {
  font-size: 0.8em;
  padding: 7px 10px 7px 10px;
  border: 2px solid #464646;
  border-radius: 8px;
  cursor: pointer;
}

.selected {
  border: 2px solid #969696;
}

@media only screen and (max-width: 500px) {
  .home_wrapper {
    padding: 120px 20px 50px 20px;
  }
}
</style>