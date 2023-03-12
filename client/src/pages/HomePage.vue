<script setup>
import {useCollection} from "vuefire"
import {useRoute, useRouter} from 'vue-router'

import '../styles/globals.css'
import DbHelper from "@/pages/DbHelper";
import MovieContainer from "@/components/MovieContainer";


</script>

<template>
  <!--  <DbHelper></DbHelper>-->
  <div class="feed">
    <div class="movie_grid" v-for="rating in movies" :key="rating">
      <h1 class="rating_title" v-if="rating[0]">{{ rating[0]['my_rating'] }}</h1>

      <div class="movie_container_wrapper" v-for="mov in rating" :key="mov.id">
            <MovieContainer :key="mov.id" :data="mov"></MovieContainer>
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";
import MovieLib from "../../public/assets/new_lib.json"

export default {
  data() {
    return {
      movies: [],
    }
  },
  async created() {
    this.movies = this.sortMovies()

    console.log(this.movies, "movies loaded")
  },
  methods: {
    sortMovies() {
      let movies_sorted = []

      for (let i = 10; i > 0; i--) {
        let list = []
        MovieLib.forEach((elem) => {
          if (elem.my_rating === i.toString() && elem['result_count'] !== 0) {
            list.push(elem)
          }
        })
        movies_sorted.push(list)
      }
      return movies_sorted

    },
  }
}
</script>

<style scoped>
.feed {
  /*outline: 1px solid blue;*/

  position: relative;

  width: 80%;
  margin: auto;

  display: flex;
  flex-direction: column;
}
.rating_title {
  width: 100%;
  font-size: 1.5em;
  border-bottom: solid black 2px;
}
.movie_grid {
  /*outline: 1px solid red;*/

  width: 100%;

  display: flex;
  justify-content: space-between;
  flex-flow: row wrap;
  margin: auto;
}

.movie_grid:last-child {
  float: right;
}
</style>