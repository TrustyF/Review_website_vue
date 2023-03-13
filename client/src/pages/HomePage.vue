<script setup>
import '../styles/globals.css'
import DbHelper from "@/pages/DbHelper";
import MovieContainer from "@/components/MovieContainer";
</script>

<template>
  <div class="filters">
    <h1 style="font-weight: bold;font-size: 1.2vw">Filters</h1>
    <div class="filter_types">
      <h1 style="text-decoration: underline;font-size: 0.9vw">Type</h1>
      <div v-for="filter in availableTypes" :key="filter">
        <label style="font-size: 0.7vw">
          <input type="checkbox" @change="swap_filter(filter);applyFilters()">
          {{ filter }}
        </label>
      </div>
    </div>

    <div class="filter_genres">
      <h1 style="text-decoration: underline;font-size: 0.9vw">Genre</h1>
      <div v-for="filter in availableGenres" :key="filter">
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
      availableTypes: ["Movie", "Animation", "Documentary"],
      filteredMovies: [],
      filters: [],
      clickCount: 0
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
      // console.log("avaialable", this.filters)
    },
    applyFilters() {
      let result = []

      //set initial list
      if (this.filters.length === 0) {
        this.filteredMovies = this.movies
        return
      }

      // iterate through all ratings
      for (let i = 0; i < 10; i++) {
        let list = this.movies[i]

        // exit if rating empty
        if (this.movies[i] === undefined) {
          continue
        }

        // special case for "Movie" filter
        // if (this.filters.includes("Movie") === true) {
        //   console.log('movies included')
        //   list = (list.filter(mov => mov['genre'].includes('Animation') === false))


        // filter genre
        this.filters.forEach((filter) => {
          list = (list.filter(mov => mov['genre'].includes(filter) === true))
        })



        result.push(list)
      }
      console.log('end')
      this.filteredMovies = result
    }
  }
}
</script>

<style scoped>
.feed {
  /*outline: 1px solid blue;*/

  position: relative;

  width: 87%;
  margin-left: 12%;

  display: flex;
  flex-direction: column;
}

.rating_title {
  width: 100%;
  font-size: 2em;
  border-bottom: solid black 1px;
}

.movie_grid {
  /*outline: 1px solid red;*/

  width: 100%;

  display: flex;
  flex-wrap: wrap;
  /*justify-content: space-between;*/
  flex-flow: row wrap;
  margin: auto;
}

.filters {
  position: fixed;
  width: 8%;
  /*height: 200px;*/

  padding: 0.75%;
  margin: 0.2% 0 0 1%;
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