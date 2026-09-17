<template>
  <header class="navbar-global">
    <router-link class="navbar-logo" :to="dashboardPath">
      <img src="/pata-branca.png" class="navbar-logo-pata" alt="" />
      <span>PetHope</span>
    </router-link>

    <nav class="navbar-menu">
      <router-link :to="dashboardPath">Início</router-link>

      <template v-if="sessao === 'ong'">
        <router-link to="/animais">Meus animais</router-link>
        <router-link to="/solicitacoes">Adoções</router-link>
        <router-link to="/atividades-ong">Voluntários</router-link>
        <router-link to="/doacoes-recebidas">Doações</router-link>
      </template>

      <template v-else>
        <router-link to="/ongs">Adotar</router-link>
        <router-link to="/minhas_adocoes">Minhas adoções</router-link>
        <router-link to="/doacoes">Doações</router-link>
        <router-link to="/perfil">Perfil</router-link>
      </template>

      <a href="#" @click.prevent="sair">Sair</a>
    </nav>
  </header>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const router = useRouter()
const sessao = ref('usuario')

const dashboardPath = computed(() => {
  if (sessao.value === 'ong') {
    return '/dashboard_ong'
  }

  return '/dashboard_adotante'
})

async function carregarSessao() {
  try {
    const { data } = await http.get('/api/auth/me')

    if (data.autenticado && data.tipo_sessao === 'ong') {
      sessao.value = 'ong'
    } else if (data.autenticado) {
      sessao.value = 'usuario'
    }
  } catch {
    sessao.value = 'usuario'
  }
}

async function sair() {
  try {
    await http.post('/api/auth/logout')
  } finally {
    router.push('/')
  }
}

onMounted(carregarSessao)
</script>

<style src="../styles/navbar.css"></style>
