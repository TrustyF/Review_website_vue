<script setup>
import '../styles/globals.css'
import DbHelper from "@/pages/DbHelper";
import MovieContainer from "@/components/MovieContainer";
</script>

<template>
  <div class="filters">
    <h1 style="font-weight: bold;font-size: 1.2vw">Filters</h1>
    <div class="filter_genres" >
      <h1 style="text-decoration: underline;font-size: 0.9vw">Genre</h1>
      <div v-for="filter in availableGenres" :key="filter">
        <label style="font-size: 0.7vw">
          <input type="checkbox" @change="swap_filter(filter);applyFilters()">
          {{ filter }}
        </label>
      </div>
    </div>

    <div class="filter_types">
      <h1 style="text-decoration: underline;font-size: 0.9vw">Type</h1>
      <div v-for="filter in availableTypes" :key="filter">
        <label style="font-size: 0.7vw">
          <input type="checkbox" @change="swap_filter(filter);applyFilters()">
          {{ filter }}
        </label>
      </div>
    </div>
  </div>
  <div class="feed">
    <div class="movie_grid" v-for="rating in filteredMovies" :key="rating">
      <h1 class="rating_title" v-if="rating[0]">{{ rating[0]['my_rating'] }}</h1>
      <div class="movie_container_wrapper" v-for="mov in rating" :key="mov.id">
        <MovieContainer :key="mov.id" :data="mov"></MovieContainer>
      </div>

    </div>
  </div>
</template>

<script>
import MovieLib from "../../public/assets/new_lib.json"

export default {
  data() {
    return {
      movies: [],
      availableGenres: ["Action", "Adventure", "Sci-Fi", "Crime", "Comedy", "Drama", "Mystery", "Thriller"],
      availableTypes: ["Animation", "Documentary"],
      filteredMovies: [],
      filters: []
    }
  },
  async created() {
    this.movies = this.sortMovies()
    this.filteredMovies = []
    this.applyFilters()
  },
  methods: {
    sortMovies() {
      let movies_sorted = []

      for (let i = 10; i > 0; i--) {
        let list = []
        MovieLib.forEach((elem) => {
          if (elem.my_rating === i.toString() && elem['result_count'] !== 0 && elem['type'] === 'Movie') {
            list.push(elem)
          }
        })
        movies_sorted.push(list)
      }
      return movies_sorted

    },
    swap_filter(filter) {
      if (this.filters.includes(filter) === false) {
        this.filters.push(filter)
      } else {
        let index = this.filters.indexOf(filter)
        if (index > -1) { // only splice array when item is found
          this.filters.splice(index, 1); // 2nd parameter means remove one item only
        }
      }
      console.log("avaialable", this.filters)
    },
    applyFilters() {
      // console.log('filtering')
      let result = []

      if (this.filters.length === 0) {
        console.log('no filters')
        this.filteredMovies = this.movies
        return
      }
      console.log('filter found')
      for (let i = 0; i < 10; i++) {
        let list = this.movies[i]

        if (this.movies[i] === undefined) {
          continue
        }

        this.filters.forEach((filter) => {
          // console.log('filter', filter)
          list = (list.filter(mov => mov['genre'].includes(filter) === false))
        })

        // this.movies[i].forEach((mov) => {
        //   // console.log(i)
        //   if (mov['genre'].includes('Animation')) {
        //     console.log(mov['name'])
        //     let index = this.movies[i].indexOf(mov)
        //     if (index > -1) { // only splice array when item is found
        //       this.movies[i].splice(index, 1); // 2nd parameter means remove one item only
        //     }
        //   }
        // })
        result.push(list)

      }
      console.log('filtered', result)
      this.filteredMovies = result
    }
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

.filters {
  position: fixed;
  width: 6vw;
  /*height: 200px;*/

  padding: 15px;
  margin: 15px;
  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);

  display: flex;
  flex-flow: column;
  /*grid-template-areas:"left right";*/
  gap: 8px;
}

.filter_genres {
  /*outline: red 1px solid;*/
  /*grid-area: left;*/
  display: flex;
  flex-flow: column;
}

.filter_types {
  /*outline: green 1px solid;*/
  /*grid-area: right;*/
  display: flex;
  flex-flow: column;
}
</style>