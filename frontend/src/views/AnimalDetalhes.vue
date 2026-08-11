<template>
<div class="page-animal-detalhes">
    <div class="container" v-if="animal">
      <h1>{{ animal.nome }}</h1>

      <div class="card">
        <p><strong>Espécie:</strong> {{ animal.especie }}</p>
        <p><strong>Raça:</strong> {{ animal.raca || 'Não informada' }}</p>
        <p><strong>Idade:</strong> {{ animal.idade || 'Não informada' }}</p>
        <p><strong>Sexo:</strong> {{ animal.sexo || 'Não informado' }}</p>
        <p><strong>Descrição:</strong> {{ animal.descricao || 'Sem descrição cadastrada.' }}</p>

        <p>
          <strong>Status:</strong>
          <span v-if="animal.status === 'Disponível'">🟢 Disponível</span>
          <span v-else-if="animal.status === 'Em processo de adoção'">🟡 Em processo de adoção</span>
          <span v-else-if="animal.status === 'Adotado'">🔴 Adotado</span>
          <span v-else>⚪ Status não definido</span>
        </p>

        <div class="card-actions">
          <router-link :to="`/editar_animal/${animal.id}`" class="btn-outline">Editar</router-link>
          <button type="button" class="btn-outline" @click="excluir">Excluir</button>
        </div>
      </div>

      <router-link to="/animais" class="btn-voltar">Voltar para lista de animais</router-link>
    </div>
    <p v-else-if="erro">{{ erro }}</p>
</div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const props = defineProps({ id: { type: [String, Number], required: true } })
const router = useRouter()
const animal = ref(null)
const erro = ref('')

async function carregar() {
  try {
    const { data } = await http.get(`/api/animals/${props.id}`)
    animal.value = data
  } catch {
    erro.value = 'Animal não encontrado'
  }
}

async function excluir() {
  try {
    await http.delete(`/api/animals/${props.id}`)
    router.push('/animais')
  } catch (err) {
    erro.value = err.response?.data?.detail || 'Erro ao excluir'
  }
}

onMounted(carregar)
</script>

<style scoped src="../styles/animal_detalhes.css"></style>
