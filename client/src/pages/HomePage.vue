<script setup>
import '../styles/globals.css'
import MovieContainer from "@/components/MovieContainer";
</script>

<template>
  <div class="filters">
    <h1 style="font-weight: bold; font-size: 1.5em">Filters</h1>

    <div class="filter_types">
      <h1 style="text-decoration: underline;padding-bottom: 5px">Type</h1>
      <div v-for="filter in availableTypes" :key="filter">
        <label class="filter_label">
          <input type="checkbox" @click="swap_filter(filter,typeFilters);applyFilters()">
          {{ filter }}
        </label>
      </div>
    </div>

    <div class="filter_rating">
      <h1 style="text-decoration: underline;padding-bottom: 5px">Rating</h1>
      <div v-for="filter in availableRatings" :key="filter">
        <label class="filter_label">
          <input type="checkbox" @click="swap_filter(filter,ratingFilters);applyFilters()">
          {{ filter }}
        </label>
      </div>
    </div>

    <div class="filter_time">
      <h1 style="text-decoration: underline;padding-bottom: 5px">Length</h1>
      <div v-for="filter in availableLength" :key="filter">
        <label class="filter_label">
          <input type="checkbox" @click="swap_filter(filter,lengthFilters);applyFilters()">
          {{ filter + "h" }}
        </label>
      </div>
    </div>

    <div class="filter_genres">
      <h1 style="text-decoration: underline;padding-bottom: 5px">Genre</h1>
      <div v-for="filter in availableGenres" :key="filter">
        <label class="filter_label">
          <input type="checkbox" @click="swap_filter(filter,genreFilters);applyFilters()">
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
      availableGenres: ["Action", "Adventure", "Crime", "Comedy", "Drama", "Family", "Horror", "Mystery", "Science Fiction", "Thriller"],
      availableTypes: ["Movie", "Animation", "Tv-series", "Documentary"],
      availableRatings: [9, 8, 7, 6, 5, 4, 3, 2, 1],
      availableLength: [1, 2, 3],
      filteredMovies: [],
      genreFilters: [],
      typeFilters: [],
      lengthFilters: [],
      ratingFilters: [],
    }
  },
  async created() {
    this.movies = [...this.sortMovies()]
    this.filteredMovies = []
    this.applyFilters()
  },
  methods: {
    sortMovies() {
      let movies_sorted = []
      // console.log(MovieLib)

      for (let i = 10; i > 0; i--) {
        let list = []
        Object.keys(MovieLib).forEach((type) => {
          if (type.length > 0) {
            MovieLib[type].forEach((elem) => {
              if (elem.my_rating === i.toString() && elem['result_count'] !== 0) {
                list.push(elem)
              }
            })
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
    swap_filter(filter, target) {
      if (target.includes(filter) === false) {
        target.push(filter)
      } else {
        let index = target.indexOf(filter)
        if (index > -1) { // only splice array when item is found
          target.splice(index, 1); // 2nd parameter means remove one item only
        }
      }
    },
    applyFilters() {
      let result = []
      let ratings = []
      let reversedMovies = [...this.movies].reverse()

      if (this.ratingFilters.length < 1) {
        ratings = [1, 2, 3, 4, 5, 6, 7, 8, 9]
      } else {
        ratings = this.ratingFilters.sort()
      }
      console.log("reverse", reversedMovies)

      // filter rating
      ratings.forEach((rating) => {
        let list = reversedMovies[rating - 1]

        // filter length
        this.lengthFilters.forEach((len) => {
          let temp = (list.filter(mov => mov['media_type'].includes("tv") === false))
          list = temp.filter(mov => mov['runtime'] > len * 60 && mov['runtime'] < (len + 1) * 60)
        })

        // filter type
        this.typeFilters.forEach((type) => {
          if (type === "Tv-series") type = "tv"
          let lower_type = type.toLowerCase()
          let temp1 = (list.filter(mov => mov['media_type'].includes(lower_type) === true))
          let temp2 = (list.filter(mov => mov['genres'].includes(type) === true))
          list = temp1.concat(temp2)
        })

        // filter genre
        this.genreFilters.forEach((genre) => {
          list = (list.filter(mov => mov['genres'].includes(genre) === true))
        })

        result.push(list)
      })
      this.filteredMovies = [...result].reverse()
    },
    getRankDetails(rank) {
      if (rank === '9') return 'Near perfect masterpiece'
      if (rank === '8') return 'Extremely good'
      if (rank === '7') return 'Quite good'
      if (rank === '6') return 'Good with flaws'
      if (rank === '5') return "Mid"
      if (rank === '4') return 'Bad'
      if (rank === '3') return 'Fucking bad'
      if (rank === '2') return 'Holy shit bad'
      if (rank === '1') return 'Affront to god'
    }
  }
}
</script>

<style scoped>
.feed {
  /*outline: 1px solid blue;*/

  position: relative;


  margin-left: 250px;
  margin-right: 20px;

  display: flex;
  flex-direction: column;
}

.rating_container {
  width: 100%;
  user-select: none;
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
  transform: translate(35px, -25px);
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
  font-family: Calibri;

  user-select: none;
  position: fixed;
  width: 150px;
  font-min-size: 1em;
  /*height: 200px;*/

  padding: 20px;
  margin: 15px 0 0 25px;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);

  display: flex;
  flex-flow: column;
  /*grid-template-areas:"left right";*/
  gap: 8px;
}

.filter_label {
  font-size: 0.9em;
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