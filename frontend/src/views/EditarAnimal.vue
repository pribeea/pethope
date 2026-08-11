<template>
  <div v-if="animal" class="page-editar-animal">
    <h1>Editar Animal</h1>

    <form @submit.prevent="salvar">
      <label>Nome:</label><br />
      <input type="text" v-model="animal.nome" required /><br /><br />

      <label>Espécie:</label><br />
      <input type="text" v-model="animal.especie" required /><br /><br />

      <label>Raça:</label><br />
      <input type="text" v-model="animal.raca" /><br /><br />

      <label>Idade:</label><br />
      <input type="number" v-model.number="animal.idade" /><br /><br />

      <label>Sexo:</label><br />
      <select v-model="animal.sexo">
        <option value="Macho">Macho</option>
        <option value="Fêmea">Fêmea</option>
      </select><br /><br />

      <label>Descrição:</label><br />
      <textarea v-model="animal.descricao" rows="5" cols="40"></textarea><br /><br />

      <button type="submit">Salvar alterações</button>
    </form>

    <br />
    <router-link to="/animais">Cancelar</router-link>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const props = defineProps({ id: { type: [String, Number], required: true } })
const router = useRouter()
const animal = ref(null)

async function carregar() {
  const { data } = await http.get(`/api/animals/${props.id}`)
  animal.value = data
}

async function salvar() {
  await http.put(`/api/animals/${props.id}`, {
    nome: animal.value.nome,
    especie: animal.value.especie,
    raca: animal.value.raca,
    idade: animal.value.idade,
    sexo: animal.value.sexo,
    descricao: animal.value.descricao,
  })
  router.push('/animais')
}

onMounted(carregar)
</script>

<style scoped src="../styles/editar_animal.css"></style>
