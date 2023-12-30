<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import ExpandedHeaderRating from "@/components/MediaContainer/Expanded/Base/sub_components/ExpandedHeaderRating.vue";
import x_button from '@/assets/ui/thin_x_button.png'
import gold_star from '@/assets/ui/gold_star.png'
import blue_star from '@/assets/ui/blue_star.png'

let props = defineProps(["data"]);
let emits = defineEmits(['closed'])
const curr_api = inject("curr_api");

function conv_sec_to_time(f_seconds) {
  let minutes = f_seconds % 60
  let hours = (f_seconds - minutes) / 60
  return hours + 'h ' + minutes + 'm';
}

function emit_close() {
  emits('closed')
}

</script>

<template>
  <div class="media_expanded_wrapper">

    <img :src="x_button" alt="close_button" class="close_button" @click="emit_close">

    <div class="content">

      <img :src="`${curr_api}/media/get_image?id=${data['id']}`" class="poster" alt="poster" draggable="false">

      <div class="info">
        <div class="header">

          <h1 class="title">{{ data['name'] }}</h1>

          <div class="subtitle_wrapper">
            <h2 class="subtitle">{{ data['release_date'].substring(0, 4) }}</h2>
            <h2 class="subtitle" v-if="data['runtime']>0">{{ ' • ' + conv_sec_to_time(data['runtime']) }}</h2>
            <h2 class="subtitle" v-if="data['seasons']>0">{{ ' • ' + `${data['seasons']} ${data['seasons'] > 1 ? 'seasons' : 'season'}` }} </h2>
            <h2 class="subtitle" v-if="data['episodes']>0">{{ ' • ' + Math.round(data['episodes'] / data['seasons']) + ' episodes' }} </h2>
          </div>

        </div>

        <div class="tags">

          <div class="genres_tags">
            <div class="genre_tag" v-for="genre in data['genres']" :key="genre['id']">{{ genre['name'] }}</div>
          </div>

          <div class="rating_tags">
            <div class="rating_tag">
              <h1 class="rating_number"> {{ data['user_rating'] }} </h1>
              <img class="rating_star" :src="blue_star" alt="blue_star">
            </div>
            <div class="rating_tag">
              <h1 class="rating_number"> {{ Math.round(data['scaled_public_rating'] * 10) / 10 }} </h1>
              <img class="rating_star" :src="gold_star" alt="gold_star">
            </div>
          </div>

        </div>

        <div class="overview">
          <p class="description">{{ data['overview'] }}</p>
        </div>


      </div>

    </div>
  </div>
</template>

<style scoped>
.media_expanded_wrapper {
  position: relative;
  max-width: 1000px;

  border-radius: 10px;
  outline: 2px solid #464646;
  margin: auto;

  background: #1c1b23;
  z-index: 50;
}

.close_button {
  position: absolute;
  right: 10px;
  top: 10px;
  width: 25px;
  height: 25px;
  filter: invert() opacity(40%);
  cursor: pointer;
  z-index: 50;
}

.content {
  display: flex;
  flex-flow: row nowrap;
  position: relative;
}

.poster {
  max-width: 30%;
  border-radius: 10px;
  object-fit: cover;
  box-shadow: 5px 0 2px #131215;
}
.header {
  display: flex;
  flex-flow: column;
  gap: 3px;
}

.info {
  display: flex;
  flex-flow: column nowrap;
  justify-content: center;
  padding: 20px;
  gap: 10px;
}

.title {
  /*height: 21px;*/
  font-weight: bold;
  font-size: 1.5em;
  text-shadow: 1px 1px 3px black;
}

.subtitle_wrapper {
  display: flex;
  gap: 3px;
}

.subtitle {
  font-size: 0.9em;
  color: rgb(150, 150, 150);
}

.tags {
  display: flex;
  flex-flow: column wrap;
  gap: 7px;
}

.genres_tags {
  display: flex;
  flex-flow: row wrap;
  gap: 7px;
}

.genre_tag {
  padding: 4px;
  border-radius: 5px;
  font-size: 0.9em;
  outline: 1.5px grey solid;
  box-shadow: 2px 2px 5px #000000;
}

.rating_tags {
  display: flex;
  flex-flow: row wrap;
  gap: 7px;
}

.rating_tag {
  padding: 4px;
  border-radius: 5px;
  outline: 1.5px grey solid;
  box-shadow: 2px 2px 5px #000000;

  display: flex;
  flex-flow: row nowrap;
  text-align: center;

  align-items: center;

  gap: 2px;
}

.rating_number {
  height: 0.8em;
  font-size: 0.9em;
}

.rating_star {
  height: 0.8em;
  /*object-fit: scale-down;*/
}

.description {
  /*outline: 1px solid green;*/
  font-size: 0.8em;
  line-height: 1.3em;
  overflow-y: scroll;
  max-height: 200px;

  -ms-overflow-style: scrollbar; /* IE and Edge */
  scrollbar-width: thin; /* Firefox */
}

.description::-webkit-scrollbar {
  width: 0.2em;
}
.description::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
}
.description::-webkit-scrollbar-thumb {
  background-color: #41404d;
}
@media only screen and (max-width: 647px) {
  .title {
    font-size: 1.2em;
  }
  .subtitle {
    font-size: 0.8em;
  }
  .genre_tag {
    font-size: 0.8em;
  }
  .rating_tag {
    font-size: 0.8em;
  }

  .media_expanded_wrapper {
    max-height: 96vh;
  }
  .content {
    flex-flow: column;
  }
  .info {
  }
  .poster {
    max-width: 50%;
    margin: 20px 0 0 20px;
    object-fit: cover;
    box-shadow: 5px 5px 2px #131215;
  }
}
</style>