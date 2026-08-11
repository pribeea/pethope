<template>
<div class="page-login">
    <div class="main-wrapper">
      <div class="sidebar">
        <div class="logo-container">🐾 PETHOPE</div>
        <div class="dog-image-container">
          <img src="/imagens/img_login.png" alt="Pets" class="pet-img" />
        </div>
      </div>

      <div class="container">
        <h1>Entrar</h1>
        <p class="subtitle">Bem-vindo de volta ao PetHope! 🐾</p>

        <form @submit.prevent="entrar">
          <div class="form-group">
            <label for="email">E-mail:</label>
            <input id="email" v-model="email" type="email" required placeholder="exemplo@email.com" />
          </div>

          <div class="form-group">
            <label for="senha">Senha:</label>
            <input id="senha" v-model="senha" type="password" required placeholder="Digite sua senha" />
          </div>

          <div class="button-group">
            <button type="button" class="btn-back" @click="$router.push('/')">Voltar</button>
            <button type="submit" class="btn-next">Entrar</button>
          </div>

          <div id="mensagem" :style="{ color: cor, display: mensagem ? 'block' : 'none' }">
            {{ mensagem }}
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
const email = ref('')
const senha = ref('')
const mensagem = ref('')
const cor = ref('#27ae60')

async function entrar() {
  try {
    const { data } = await http.post('/api/auth/login', { email: email.value, senha: senha.value })
    cor.value = '#27ae60'
    mensagem.value = 'Login realizado com sucesso!'

    const destino = data.tipo === 'voluntario' ? '/dashboard_voluntario' : '/dashboard_adotante'
    setTimeout(() => router.push(destino), 1000)
  } catch (err) {
    cor.value = '#d9534f'
    mensagem.value = err.response?.data?.detail || 'Email ou senha inválidos.'
  }
}
</script>

<style scoped src="../styles/login.css"></style>
