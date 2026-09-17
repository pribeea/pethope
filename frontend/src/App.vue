<template>
  <Navbar v-if="mostrarNavbar" />
  <router-view />
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'

const route = useRoute()

const rotasPublicas = [
  'home',
  'cadastro',
  'opcoes_login',
  'login',
  'cadastro_ong',
  'login_ong'
]

const mostrarNavbar = computed(() => !rotasPublicas.includes(route.name))
</script>
