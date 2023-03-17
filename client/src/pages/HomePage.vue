<script setup>
import '../styles/globals.css'
import MovieContainer from "@/components/MovieContainer";
</script>

<template>
  <div class="filters">
    <h1 style="font-weight: bold; font-size: 1.5em">Filters</h1>
    <label class="filter_label">
      <input type="checkbox" style="cursor: pointer" @click="excludeMode = !excludeMode">
      Invert
    </label>

    <div class="filter_types" v-for="elem in filters" :key="elem['name']">
      <h1 style="text-decoration: underline;padding-bottom: 5px">{{ elem['name'] }}</h1>
      <div v-for="filter in elem['available']" :key="filter" class="filter_content_list">
        <label class="filter_label">
          <input type="checkbox" style="cursor: pointer" @click="swap_filter(filter,elem['filter']);">
          {{ filter }}
        </label>
      </div>
    </div>

  </div>
  <div class="feed">
    <div class="movie_grid" v-for="rating in computeFilters" :key="rating">

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
      filteredMovies: [],
      filters: {
        'type': {
          'name': 'Type',
          'available': ["Movie", "Tv-series"],
          'filter': [],
        },
        'format': {
          'name': 'Format',
          'available': ["Live-action", "Animated", "Documentary"],
          'filter': [],
        },
        'genre': {
          'name': 'Genre',
          'available': ["Action", "Adventure", "Crime", "Comedy", "Drama", "Family", "Horror", "Mystery", "Science Fiction", "Thriller"],
          'filter': [],
        },
        'rating': {
          'name': 'Rating',
          'available': [9, 8, 7, 6, 5, 4, 3, 2, 1],
          'filter': [],
        },
        'length': {
          'name': 'Length',
          'available': [1, 2, 3],
          'filter': [],
        },
      },
      excludeMode: false
    }
  },
  async created() {
    this.movies = [...this.sortMovies()]
    this.filteredMovies = []
  },
  computed: {
    computeFilters() {
      return this.applyFilters()
    }
  },
  methods: {
    sortMovies() {
      let movies_sorted = []

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
    },
    applyFilters() {
      let result = []
      let ratings = []
      let reversedMovies = [...this.movies].reverse()

      let f_type = this.filters['type']['filter']
      let f_format = this.filters['format']['filter']
      let f_genre = this.filters['genre']['filter']
      let f_rating = this.filters['rating']['filter']
      let f_length = this.filters['length']['filter']

      let exclude_mode = this.excludeMode

      let lenMin
      let lenMax
      if (f_length.length > 0) {
        lenMin = Math.min(...f_length)
        lenMax = Math.max(...f_length)
      }

      if (f_rating.length < 1) {
        ratings = [1, 2, 3, 4, 5, 6, 7, 8, 9]
      } else {
        ratings = f_rating.sort()
      }

      // filter rating
      ratings.forEach((rating) => {
        let list = reversedMovies[rating - 1]

        // filter length
        if (f_length.length > 0) {
          list = (list.filter(mov => mov['runtime'] > lenMin * 60 && mov['runtime'] < (lenMax + 1) * 60 && mov['media_type'].includes("tv") === exclude_mode))
        }

        // filter type
        f_type.forEach((type) => {
          // filter movies
          if (type === "Movie") {
            list = list.filter(mov => mov['media_type'].includes("movie") === !exclude_mode)
          }
          // filter tv
          if (type === "Tv-series") {
            list = list.filter(mov => mov['media_type'].includes("tv") === !exclude_mode)
          }
        })

        // filter format
        f_format.forEach((format) => {
          // filter Live-action
          if (format === "Live-action") {
            list = list.filter(mov => mov['genres'].includes("Animation") === exclude_mode)
          }
          // filter Animated
          if (format === "Animated") {
            list = list.filter(mov => mov['genres'].includes("Animation") === !exclude_mode)
          }
          // filter Documentary
          if (format === "Documentary") {
            list = list.filter(mov => mov['genres'].includes("Documentary") === !exclude_mode)
          }
        })

        // filter genre
        f_genre.forEach((genre) => {
          list = (list.filter(mov => mov['genres'].includes(genre) === !exclude_mode))
        })

        result.push(list)
      })
      // this.filteredMovies = [...result].reverse()
      return result.reverse()
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

.filter_content_list {
  outline: red 1px solid;
  width: 100%;
}

.filter_label {
  font-size: 0.9em;
  cursor: pointer;
}
</style>