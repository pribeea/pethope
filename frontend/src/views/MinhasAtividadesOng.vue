<template>
  <div class="page-lista-atividades">
    <header>
      <h2>
        <img src="/pata-branca.png" class="logo-pata" alt="" />
        PetHope
      </h2>

      <a href="#" @click.prevent="sair">Sair</a>
    </header>

    <div class="main-wrapper">

      <div class="header-section">
        <h2>Minhas atividades</h2>

        <p class="subtitle">
          Gerencie as atividades de voluntariado cadastradas pela sua ONG.
        </p>
      </div>

      <div v-if="carregando" class="loading">
        <p>🔄 Carregando atividades...</p>
      </div>

      <div v-else-if="erro" class="erro">
        <p>❌ {{ erro }}</p>
      </div>

      <div v-else class="cards-container">

        <article
          v-if="atividades.length"
          v-for="atividade in atividades"
          :key="atividade.id"
          class="atividade-card"
        >
          <template v-if="atividadeEditando !== atividade.id">

            <div class="atividade-info">

              <div class="atividade-topo">
                <h3>{{ atividade.titulo }}</h3>
              </div>

              <p>
                <strong>Descrição:</strong>
                {{ atividade.descricao }}
              </p>

              <div class="informacoes">

                <span>
                  <strong>Dias:</strong>
                  {{ atividade.dias }}
                </span>

                <span>
                  <strong>Horário:</strong>
                  {{ atividade.horario }}
                </span>

                <span>
                  <strong>Vagas:</strong>
                  {{ atividade.vagas }}
                </span>

              </div>

              <div v-if="atividade.detalhes" class="detalhes">
                <strong>Detalhes:</strong>
                {{ atividade.detalhes }}
              </div>

              <div class="acoes">

                <router-link
                  class="btn btn-voluntarios"
                  :to="{ name: 'inscricoes_atividade', params: { atividadeId: atividade.id } }"
                >
                  Ver voluntários
                </router-link>

                <button
                  type="button"
                  class="btn btn-editar"
                  @click="iniciarEdicao(atividade)"
                >
                  Editar
                </button>

                <button
                  type="button"
                  class="btn btn-excluir"
                  @click="excluirAtividade(atividade.id)"
                >
                  Excluir
                </button>

              </div>

            </div>

          </template>

          <template v-else>

            <div class="atividade-info">

              <form class="form-edicao" @submit.prevent="salvarEdicao">

                <h3>Editar atividade</h3>

                <div class="form-group">

                  <label>Título</label>

                  <input
                    v-model="formulario.titulo"
                    type="text"
                    required
                    maxlength="150"
                  />

                </div>

                <div class="form-group">

                  <label>Descrição</label>

                  <textarea
                    v-model="formulario.descricao"
                    required
                    maxlength="1000"
                    rows="4"
                  ></textarea>

                </div>

                <div class="campos-linha">

                  <div class="form-group">

                    <label>Dias</label>

                    <input
                      v-model="formulario.dias"
                      type="text"
                      required
                      maxlength="100"
                    />

                  </div>


                  <div class="form-group">

                    <label>Horário</label>

                    <input
                      v-model="formulario.horario"
                      type="text"
                      required
                      maxlength="100"
                    />

                  </div>


                  <div class="form-group campo-vagas">

                    <label>Vagas</label>

                    <input
                      v-model.number="formulario.vagas"
                      type="number"
                      min="1"
                      max="1000"
                      required
                    />

                  </div>

                </div>

                <div class="form-group">

                  <label>Detalhes</label>

                  <textarea
                    v-model="formulario.detalhes"
                    maxlength="3000"
                    rows="4"
                  ></textarea>

                </div>

                <div v-if="erroEdicao" class="erro-form">
                  {{ erroEdicao }}
                </div>

                <div class="acoes-edicao">

                  <button
                    type="button"
                    class="btn btn-cancelar"
                    @click="cancelarEdicao"
                    :disabled="salvando"
                  >
                    Cancelar
                  </button>

                  <button
                    type="submit"
                    class="btn btn-salvar"
                    :disabled="salvando"
                  >
                    {{ salvando ? 'Salvando...' : 'Salvar alterações' }}
                  </button>
                </div>
              </form>
            </div>
          </template>
        </article>
        <div v-else class="empty-state">
          <p>Nenhuma atividade cadastrada no momento.</p>
        </div>
      </div>

      <div class="footer-actions">
        <router-link to="/dashboard_ong" class="btn-back">
          Voltar
        </router-link>
      </div>
    </div>
  </div>
</template>


<script setup>

import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const router = useRouter()

const atividades = ref([])
const carregando = ref(true)
const erro = ref('')

const atividadeEditando = ref(null)

const formulario = ref({
  titulo: '',
  descricao: '',
  dias: '',
  horario: '',
  vagas: 1,
  detalhes: ''
})

const salvando = ref(false)
const erroEdicao = ref('')

async function carregar() {

  try {
    const { data: sessao } = await http.get('/api/auth/me')
    if (!sessao.autenticado || sessao.tipo_sessao !== 'ong') {
      router.push('/login_ong')
      return
    }

    const { data } = await http.get('/api/atividades/minhas-ong')
    atividades.value = data

  } catch (err) {
    console.error(err)
    erro.value = err.response?.data?.detail || 'Não foi possível carregar suas atividades.'

  } finally {
    carregando.value = false
  }
}

function iniciarEdicao(atividade) {

  atividadeEditando.value = atividade.id
  erroEdicao.value = ''

  formulario.value = {
    titulo: atividade.titulo || '',
    descricao: atividade.descricao || '',
    dias: atividade.dias || '',
    horario: atividade.horario || '',
    vagas: atividade.vagas || 1,
    detalhes: atividade.detalhes || ''
  }

}

function cancelarEdicao() {

  atividadeEditando.value = null
  erroEdicao.value = ''

}

async function salvarEdicao() {

  if (!atividadeEditando.value) {
    return
  }

  salvando.value = true
  erroEdicao.value = ''

  try {
    const { data } = await http.put(
      `/api/atividades/${atividadeEditando.value}`,
      formulario.value
    )
    const indice = atividades.value.findIndex(
      atividade => atividade.id === atividadeEditando.value
    )
    if (indice !== -1) {
      atividades.value[indice] = data
    }
    atividadeEditando.value = null

  } catch (err) {
    console.error(err)
    erroEdicao.value = err.response?.data?.detail || 'Não foi possível salvar as alterações.'
  } finally {
    salvando.value = false
  }
}

async function excluirAtividade(atividadeId) {

  const confirmar = window.confirm(
    'Tem certeza que deseja excluir esta atividade?\n\n' +
    'A atividade será removida e as inscrições dos voluntários também serão excluídas.'
  )

  if (!confirmar) {
    return
  }

  try {
    await http.delete(`/api/atividades/${atividadeId}`)
    atividades.value = atividades.value.filter(
      atividade => atividade.id !== atividadeId
    )

  } catch (err) {
    console.error(err)
    alert(
      err.response?.data?.detail ||
      'Não foi possível excluir a atividade.'
    )
  }
}

async function sair() {
  try {
    await http.post('/api/auth/logout')
    router.push('/')

  } catch (err) {
    console.error(err)
  }
}

onMounted(carregar)

</script>

<style scoped src="../styles/minhas_atividades_ong.css"></style>