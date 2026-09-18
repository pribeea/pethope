<template>
<div class="page-animal-detalhes">
    <div class="detalhe-intro">
      <h1>Detalhes do animal</h1>
      <p>Conheça melhor esse pet e veja as opções disponíveis.</p>
    </div>

    <div class="detalhe-card" v-if="animal">
      <div v-if="animal.foto" class="detalhe-foto">
        <img :src="urlFoto(animal.foto)" :alt="`Foto de ${animal.nome}`" />
      </div>
      <div v-else class="detalhe-foto sem-foto">
        <span>🐾</span>
      </div>

      <div class="detalhe-info">
        <h2>{{ animal.nome }}</h2>

        <p><strong>Espécie:</strong> {{ animal.especie }}</p>
        <p><strong>Raça:</strong> {{ animal.raca || 'Não informada' }}</p>
        <<p><strong>Idade:</strong> {{ animal.idade ? `${animal.idade} ${animal.unidade_idade || ''}` : 'Não informada' }}</p>
        <p><strong>Sexo:</strong> {{ animal.sexo || 'Não informado' }}</p>
        <p><strong>Descrição:</strong> {{ animal.descricao || 'Sem descrição cadastrada.' }}</p>

        <p>
          <strong>Status:</strong>
          <span v-if="animal.status === 'Disponível'">🟢 Disponível</span>
          <span v-else-if="animal.status === 'Em processo de adoção'">🟡 Em processo de adoção</span>
          <span v-else-if="animal.status === 'Adotado'">🔴 Adotado</span>
          <span v-else>⚪ Status não definido</span>
        </p>

        <div v-if="papel === 'ong'" class="detalhe-acoes acoes-ong">
          <router-link :to="`/editar_animal/${animal.id}`" class="btn-outline">Editar</router-link>
          <button type="button" class="btn-outline btn-excluir" @click="excluir">Excluir</button>
        </div>

        <div v-else class="detalhe-acoes">
          <button
            type="button"
            class="btn-adotar"
            :disabled="animal.status !== 'Disponível'"
            @click="router.push(`/adotar/${animal.id}`)"
          >
            Quero adotar
          </button>
        </div>
      </div>
    </div>

    <p v-else-if="erro" class="erro-msg">{{ erro }}</p>

    <router-link :to="rotaVoltar" class="btn-voltar">
      {{ textoVoltar }}
    </router-link>
</div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import http from '../api/http'

const props = defineProps({ id: { type: [String, Number], required: true } })
const router = useRouter()
const route = useRoute()
const animal = ref(null)
const erro = ref('')
const papel = ref('usuario')
const rotaVoltar = ref('/ongs')
const textoVoltar = ref('Voltar para as ONGs')

function urlFoto(caminho) {
  if (!caminho) {
    return ''
  }

  if (caminho.startsWith('http')) {
    return caminho
  }

  const baseURL = http.defaults.baseURL || 'http://localhost:8000'

  return `${baseURL}${caminho}`
}

async function carregarSessao() {
  try {
    const { data } = await http.get('/api/auth/me')
    if (data.autenticado && data.tipo_sessao === 'ong') {
      papel.value = 'ong'
    } else {
      papel.value = 'usuario'
    }

    if (papel.value === 'ong') {
      rotaVoltar.value = '/dashboard_ong'
      textoVoltar.value = 'Voltar para o dashboard'
    } else if (route.query.ongId) {
      rotaVoltar.value = `/ongs/${route.query.ongId}/animais`
      textoVoltar.value = 'Voltar para os animais da ONG'
    } else {
      rotaVoltar.value = '/ongs'
      textoVoltar.value = 'Voltar para as ONGs'
    }
  } catch {
    papel.value = 'usuario'
  }
}

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
    router.push('/dashboard_ong')
  } catch (err) {
    erro.value = err.response?.data?.detail || 'Erro ao excluir'
  }
}

onMounted(() => {
  carregarSessao()
  carregar()
})
</script>

<style scoped src="../styles/animal_detalhes.css"></style>
