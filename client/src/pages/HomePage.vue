<script setup>
import '../styles/globals.css'
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
      <div v-if="rating[0]" class="rating_container">
        <h1 class="rating_title">{{ rating[0]['my_rating'] }}</h1>
        <p class="rating_desc"> {{ getRankDetails(rating[0]['my_rating']) }}</p>
      </div>
      <div class="movie_container_wrapper" v-for="mov in rating" :key="mov.id">
        <MovieContainer :key="mov.id" :data="mov"></MovieContainer>
      </div>

    </div>
  </div>
</template>

<script>
import MovieLib from "../../public/assets/movie_db_lib.json"

export default {
  data() {
    return {
      movies: [],
      availableGenres: ["Action", "Adventure", "Science Fiction", "Crime", "Comedy", "Drama", "Horror", "Mystery", "Thriller"],
      availableTypes: ["Movie", "Animation", "Documentary"],
      filteredMovies: [],
      filters: [],
    }
  },
  async created() {
    this.movies = [...this.sortMovies()]
    this.filteredMovies = []
    await this.applyFilters()
  },
  methods: {
    sortMovies() {
      let movies_sorted = []
      // console.log(MovieLib)

      for (let i = 10; i > 0; i--) {
        let list = []
        MovieLib['movie_results'].forEach((elem) => {
          if (elem.my_rating === i.toString() && elem['result_count'] !== 0) {
            list.push(elem)
          }
        })
        // sort by reception
        list.sort((a, b) => b['vote_average'] - a['vote_average'])
        // export
        movies_sorted.push(list)
      }
      console.log(movies_sorted)
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
    },
    async applyFilters() {
      let result = []

      //set initial list
      if (this.filters.length === 0) {
        this.filteredMovies = [...this.movies]
        return
      }

      // iterate through all ratings
      for (let i = 0; i < 10; i++) {
        let list = this.movies[i]

        // exit if rating empty
        if (list === undefined) {
          continue
        }


        // special case for "Movie" filter
        if (this.filters.includes("Movie") === true) {
          // filter genre only movies
          const excludeFilters = ['Animation', 'Documentary']
          excludeFilters.forEach((filter) => {
            list = (list.filter(mov => mov['genres'].includes(filter) === false))
          })

          let tempFilter = [...this.filters]
          let index = tempFilter.indexOf("Movie")
          if (index > -1) {
            tempFilter.splice(index, 1);
          }

          if (tempFilter.length !== 0) {
            tempFilter.forEach((filter) => {
              list = (list.filter(mov => mov['genres'].includes(filter) === true))
            })
          }
        } else {
          // filter genre
          this.filters.forEach((filter) => {
            list = (list.filter(mov => mov['genres'].includes(filter) === true))
          })
        }


        result.push(list)
      }
      this.filteredMovies = result
    },
    getRankDetails(rank) {
      if (rank === '9')  return 'Near perfect masterpiece'
      if (rank === '8')  return 'Extremely good'
      if (rank === '7')  return 'Quite good'
      if (rank === '6')  return 'Good with minor flaws'
      if (rank === '5')  return "I didn't like"
      if (rank === '4')  return 'Bad'
      if (rank === '3')  return 'Bad and boring'
      if (rank === '2')  return 'Holy shit bad'
      if (rank === '1')  return 'Affront to god'
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

.rating_container {
  width: 100%;
}

.rating_title {
  font-family: "Arial Black";
  padding: 10px 5px 5px 0;
  font-size: 2em;
  border-bottom: solid black 1px;
}

.rating_desc {
  /*font-family: Calibri;*/
  font-size: 1em;
  position: absolute;
  transform: translate(35px,-25px);
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