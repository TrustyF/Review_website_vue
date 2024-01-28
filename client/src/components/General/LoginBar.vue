<script setup>
import {inject, onMounted, watch, ref, computed} from "vue";
import {login, logout, check_admin, get_current_user} from "@/firebase_auth.js";

let props = defineProps(["test"]);
let emits = defineEmits(["test"]);

const curr_api = inject("curr_api");
let edit_mode = inject('edit_mode')

let logged = ref(false)

async function check_logged() {
  logged.value = await get_current_user()
}

async function handle_login() {
  await login()
  await check_logged()
  await check_edit_mode()
}

async function handle_logout() {
  await logout()
  await check_logged()
  await check_edit_mode()
}

async function check_edit_mode() {
  edit_mode.value = !!await check_admin(curr_api);
}

onMounted(() => {
  check_logged()
  check_edit_mode()
})
</script>

<template>
  <h1 class="link" v-if="!logged" @click="handle_login">Admin Login</h1>
  <h1 class="link" v-if="logged" @click="handle_logout">Logout</h1>
</template>
<style scoped>
.link {
  cursor: pointer;
}
</style>