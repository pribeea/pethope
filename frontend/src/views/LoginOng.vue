<template>
<div class="page-login-ong">
    <div class="main-wrapper">
      <div class="sidebar">
        <div class="logo-container">🐾 PETHOPE</div>
        <div class="dog-image-container">
          <img src="/imagens/img_login.png" alt="ONG" class="pet-img" />
        </div>
      </div>

      <div class="container">
        <h1>Login da ONG</h1>
        <p class="subtitle">Entre para gerenciar seus pets e adoções 🐾</p>

        <form @submit.prevent="entrar">
          <div class="form-group">
            <label for="cnpj">CNPJ:</label>
            <input id="cnpj" v-model="cnpj" type="text" required placeholder="Digite o CNPJ" />
          </div>

          <div class="form-group">
            <label for="senha">Senha:</label>
            <input id="senha" v-model="senha" type="password" required placeholder="Digite sua senha" />
          </div>

          <div class="button-group">
            <button type="button" class="btn-back" @click="$router.back()">Voltar</button>
            <button type="submit" class="btn-next">Entrar</button>
          </div>

          <div id="msg" :style="{ color: cor, display: msg ? 'block' : 'none' }">
            {{ msg }}
          </div>
        </form>
      </div>
    </div>
</div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const router = useRouter()
const cnpj = ref('')
const senha = ref('')
const msg = ref('')
const cor = ref('#27ae60')

async function entrar() {
  try {
    await http.post('/api/ongs/login', { cnpj: cnpj.value, senha: senha.value })
    cor.value = '#27ae60'
    msg.value = 'Login realizado com sucesso!'
    setTimeout(() => router.push('/dashboard_ong'), 1000)
  } catch (err) {
    cor.value = '#d9534f'
    msg.value = err.response?.data?.detail || 'CNPJ ou senha inválidos'
  }
}
</script>

<style scoped src="../styles/login_ong.css"></style>
