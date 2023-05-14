<script setup>
import '../styles/globals.css'
import MovieContainer from "@/components/MovieContainer/MovieContainer";
import DbHelper from "@/components/DbHelper";
import FilterMenu from "@/components/Homepage/FilterMenu";
import RatingHeader from "@/components/Homepage/RatingHeader";
import {inject, watch} from 'vue'

import axios from 'axios'
import {ref, onMounted} from 'vue'

const current_api = inject('curr_api')
const devMode = inject('devMode')
</script>

<template>
  <FilterMenu @filters="update_manga"></FilterMenu>
</template>

<script>
export default {
  name: "MangaPage"
}
</script>