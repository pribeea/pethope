<template>
<div class="page-cadastro-animal">
    <div class="main-wrapper">
      <div class="sidebar">
        <div class="logo-container">🐾 PETHOPE</div>
        <div class="dog-image-container">
          <img src="/imagens/img_cadastro.jpg" alt="Pets" class="pet-img" />
        </div>
      </div>

      <div class="container">
        <h1>Cadastrar Animal</h1>
        <p class="subtitle">Registre um novo amigo para encontrar um lar. 🐾</p>

        <form @submit.prevent="cadastrar">
          <div class="form-group">
            <label for="nome">Nome:</label>
            <input id="nome" v-model="form.nome" type="text" required placeholder="Nome do animal" />
          </div>

          <div class="form-row">
            <div class="form-group half">
              <label for="especie">Espécie:</label>
              <input id="especie" v-model="form.especie" type="text" required placeholder="Ex: Cachorro" />
            </div>
            <div class="form-group half">
              <label for="raca">Raça:</label>
              <input id="raca" v-model="form.raca" type="text" placeholder="Ex: Poodle" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group half">
              <label for="idade">Idade:</label>
              <input id="idade" v-model.number="form.idade" type="number" placeholder="Anos" />
            </div>
            <div class="form-group half">
              <label for="sexo">Sexo:</label>
              <input id="sexo" v-model="form.sexo" type="text" placeholder="Macho/Fêmea" />
            </div>
          </div>

          <div class="form-group">
            <label for="descricao">Descrição:</label>
            <textarea id="descricao" v-model="form.descricao" placeholder="Conte um pouco sobre o pet..."></textarea>
          </div>

          <div class="button-group">
            <button type="button" class="btn-back" @click="$router.back()">Voltar</button>
            <button type="submit" class="btn-next">Cadastrar</button>
          </div>

          <p id="msg" :style="{ color: '#d9534f' }">{{ msg }}</p>
        </form>
      </div>
    </div>
</div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const router = useRouter()

const form = reactive({
  nome: '',
  especie: '',
  raca: '',
  idade: null,
  sexo: '',
  descricao: '',
})

const msg = ref('')

async function cadastrar() {
  try {
    await http.post('/api/animals', form)
    router.push('/animais')
  } catch (err) {
    msg.value = err.response?.data?.detail || 'Erro ao cadastrar'
  }
}
</script>

<style scoped src="../styles/cadastro_animal.css"></style>
