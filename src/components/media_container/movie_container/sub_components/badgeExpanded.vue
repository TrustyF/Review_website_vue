<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";

let props = defineProps(["data", "text_size", "text_limit"]);
let emits = defineEmits(["test"]);
const curr_api = inject("curr_api");

const tier_details = computed(() => {
  let tier = props['data']['tier']

  if (tier === 'purple') return 'Warning'
  if (tier === 'green') return 'Positive'
  if (tier === 'red') return 'Negative'
  if (tier === 'gold') return 'Peak'
  if (tier === 'silver') return 'Gripe'

  return undefined
})

function add_line_breaks(content) {
  let replaced = content
  // let regEx = new RegExp(/(.{10}[^ ]* )/g)
  let regEx = new RegExp(/(.{30}[^ ]* )/g)
  replaced = replaced.replace(regEx, "$1\n")
  // replaced = replaced.replace(/\./g, `\n`)

  return replaced
}

function add_line_break_v2(content) {
  return content
}
</script>

<template>
  <div ref="tooltip_container" class="tag_tooltip" v-if="data!==undefined">

    <img v-if="data['tier']" class="tag_preview" :src="`${curr_api}/static/tags/icons/${data['tier']}/${data['image_path']}.webp`">

    <div class="tooltip_content">

      <div style="display:flex;gap: 7px;align-items: center">
        <h1 class="title">{{ data['name'] }}</h1>
        <h1 class="title_detail">{{ tier_details }}</h1>
      </div>

      <h1 class="description">{{ add_line_break_v2(data['overview']) }}</h1>

    </div>

    <!--    <div class="tag_tooltip_arrow"></div>-->

  </div>
  <div v-else class="tag_tooltip">no data</div>

</template>

<style scoped>
.tag_tooltip {
  /*position: absolute;*/
  overflow: hidden;
  /*background: linear-gradient(to left, #41404d 60%, #605c57 100%);*/

  box-shadow: 0 0 calc(v-bind(text_size) * 8px) #191726;
  border-radius: calc(v-bind(text_size) * 50px);
  background-color: #2b2a34;

  z-index: 300;

  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  gap: calc(v-bind(text_size) * 10px);

  /*height: calc(v-bind(text_size) * 4em);*/

  opacity: 0;
  visibility: hidden;
  transition: 300ms;
}

.tag_tooltip:after {
  content: "";
  height: 100%;
  padding: 0 calc(v-bind(text_size) * 15px) 0 0;
}

.tag_tooltip_arrow {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -10px;
  border-width: 10px;
  border-style: solid;
  border-color: #2b2a34 transparent transparent transparent;
}

.tooltip_content {
  display: flex;
  flex-flow: column nowrap;
  align-items: flex-start;
  gap: calc(v-bind(text_size) * 5px);
  padding: calc(v-bind(text_size) * 10px) 0 calc(v-bind(text_size) * 10px) 0;
}

.title {
  font-size: calc(v-bind(text_size) * 1em);
  font-weight: 700;
  /*color: black;*/
  text-shadow: 1px 1px calc(v-bind(text_size) * 3px) black, 0 0 calc(v-bind(text_size) * 5px) black;
}

.title_detail {
  font-size: calc(v-bind(text_size) * 0.6em);
  border: 1px #696969 solid;
  padding: 5px;
  font-weight: 300;
  color: #808080;
  border-radius: calc(v-bind(text_size) * 0.5em);
  margin-bottom: calc(v-bind(text_size) * -1px);
  /*height:calc(v-bind(text_size) * 0.6em) ;*/
  /*text-shadow: 1px 1px calc(v-bind(text_size) * 3px) black, 0 0 calc(v-bind(text_size) * 5px) black;*/
}

.description {
  font-size: calc(v-bind(text_size) * 0.8em);
  color: #b0b0b0;
  text-shadow: 0 0 calc(v-bind(text_size) * 7px) black;
  /*word-break: break-word;*/
}

.tag_preview {
  height: calc(v-bind(text_size) * 4em);
  /*width: 100%;*/
  filter: drop-shadow(0 0 calc(v-bind(text_size) * 5px) rgba(0, 0, 0, 0.75));
}
</style>