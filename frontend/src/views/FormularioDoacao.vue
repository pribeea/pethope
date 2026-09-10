<template>
<div class="page-formulario-doacao">
    <div class="container">
      <h1>💜 Fazer uma doação</h1>
      <p v-if="ong">para <strong>{{ ong.nome }}</strong></p>

      <form @submit.prevent="enviar">
        <div class="form-group">
          <label for="valor">Valor da doação (R$):</label>
          <input
            id="valor"
            v-model.number="form.valor"
            type="number"
            min="1"
            step="0.01"
            required
            placeholder="Ex: 20.00"
          />
        </div>

        <div class="valores-sugeridos">
          <button
            type="button"
            class="chip-valor"
            v-for="v in valoresSugeridos"
            :key="v"
            :class="{ ativo: form.valor === v }"
            @click="form.valor = v"
          >
            R$ {{ v }}
          </button>
        </div>

        <div class="form-group">
          <label for="nome">Seu nome (opcional):</label>
          <input
            id="nome"
            v-model="form.nome"
            type="text"
            placeholder="Deixe em branco para doar anonimamente"
          />
        </div>

        <p v-if="erro" class="erro-form">❌ {{ erro }}</p>

        <div class="button-group">
          <button type="button" class="btn-back" @click="$router.back()">Voltar</button>
          <button type="submit" class="btn-next" :disabled="enviando">
            {{ enviando ? 'Gerando pagamento...' : 'Gerar pagamento' }}
          </button>
        </div>
      </form>
    </div>
</div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const props = defineProps({ ongId: { type: [String, Number], required: true } })
const router = useRouter()

const ong = ref(null)
const erro = ref('')
const enviando = ref(false)
const valoresSugeridos = [10, 20, 50, 100]

const form = reactive({
  valor: 20,
  nome: '',
})

async function carregarOng() {
  try {
    const { data } = await http.get(`/api/ongs/${props.ongId}`)
    ong.value = data
  } catch (err) {
    console.error('Erro ao carregar ONG:', err)
  }
}

async function enviar() {
  erro.value = ''
  enviando.value = true

  try {
    const { data } = await http.post('/api/doacoes', {
      ong_id: Number(props.ongId),
      valor: form.valor,
      nome_doador: form.nome || undefined,
    })
    router.push({ name: 'pagamento_doacao', params: { id: data.id } })
  } catch (err) {
    console.error('Erro ao gerar doação:', err)
    erro.value = err.response?.data?.detail || 'Erro ao gerar o pagamento. Tente novamente.'
  } finally {
    enviando.value = false
  }
}

onMounted(carregarOng)
</script>

<style scoped src="../styles/formulario_doacao.css"></style>
