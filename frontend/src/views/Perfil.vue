<template>
  <div class="page-perfil">

    <main class="conteudo-perfil">

      <section class="cabecalho-perfil">

        <div class="foto-perfil-area">

          <div class="foto-perfil">

            <img
              v-if="dados.foto"
              :src="urlFoto(dados.foto)"
              alt="Foto de perfil"
            />

            <img
              v-else
              src="/pata-branca.png"
              alt="Foto de perfil"
              class="foto-padrao"
            />

          </div>

          <label class="btn-foto">
            Alterar foto
            <input
              type="file"
              accept="image/*"
              @change="selecionarFoto"
            />
          </label>

        </div>


        <div class="cabecalho-info">

          <p class="tipo-perfil">
            {{ textoTipo }}
          </p>

          <h1>{{ dados.nome || 'Usuário' }}</h1>

          <p class="descricao-perfil">
            Confira e gerencie as informações da sua conta no PetHope.
          </p>

        </div>

      </section>


      <!-- INFORMAÇÕES DA CONTA -->

      <section class="card-perfil">

        <h2>Informações da conta</h2>

        <div class="informacoes">

          <div class="informacao">

            <span class="rotulo">
              Nome
            </span>

            <strong>
              {{ dados.nome || 'Não informado' }}
            </strong>

          </div>


          <div class="informacao">

            <span class="rotulo">
              Tipo de conta
            </span>

            <strong>
              {{ textoTipo }}
            </strong>

          </div>

          <div
            v-if="tipoSessao === 'ong'"
            class="informacao"
          >

            <span class="rotulo">
              Endereço
            </span>

            <strong>
              {{ dados.endereco || 'Não informado' }}
            </strong>

          </div>


          <div
            v-if="tipoSessao === 'ong'"
            class="informacao"
          >

            <span class="rotulo">
              Contato
            </span>

            <strong>
              {{ dados.contato || 'Não informado' }}
            </strong>

          </div>

        </div>

      </section>


      <!-- SOBRE A CONTA -->

      <section class="card-perfil">

        <h2>
          {{ tipoSessao === 'ong' ? 'Sobre a ONG' : 'Sobre você' }}
        </h2>

        <p class="texto-card">

          <template v-if="tipoSessao === 'ong'">
            Este é o perfil da sua ONG no PetHope. Mantenha suas
            informações atualizadas para facilitar o contato com
            adotantes e voluntários.
          </template>

          <template v-else-if="dados.tipo_usuario === 'voluntario'">
            Como voluntário, você pode participar das atividades
            cadastradas pelas ONGs e contribuir com a causa animal.
          </template>

          <template v-else>
            Como adotante, você pode conhecer os animais disponíveis,
            acompanhar suas adoções e contribuir com as ONGs parceiras.
          </template>

        </p>

      </section>


      <!-- ATIVIDADE -->

      <section class="card-perfil">

        <h2>Minha atividade</h2>

        <div class="atividade-grid">

          <router-link
            v-if="tipoSessao === 'usuario'"
            to="/minhas_adocoes"
            class="atividade"
          >

            <span class="atividade-icone">
              🐾
            </span>

            <div>
              <strong>Minhas adoções</strong>

              <p>
                Acompanhe suas solicitações de adoção.
              </p>
            </div>

          </router-link>


          <router-link
            v-if="tipoSessao === 'usuario'"
            to="/doacoes"
            class="atividade"
          >

            <span class="atividade-icone">
              💜
            </span>

            <div>
              <strong>Minhas doações</strong>

              <p>
                Veja suas contribuições para as ONGs.
              </p>
            </div>

          </router-link>


          <router-link
            v-if="tipoSessao === 'ong'"
            to="/animais"
            class="atividade"
          >

            <span class="atividade-icone">
              🐶
            </span>

            <div>
              <strong>Meus animais</strong>

              <p>
                Gerencie os animais cadastrados pela ONG.
              </p>
            </div>

          </router-link>


          <router-link
            v-if="tipoSessao === 'ong'"
            to="/solicitacoes"
            class="atividade"
          >

            <span class="atividade-icone">
              🏠
            </span>

            <div>
              <strong>Solicitações de adoção</strong>

              <p>
                Confira as solicitações recebidas.
              </p>
            </div>

          </router-link>

        </div>

      </section>


      <!-- SAIR -->

      <section class="card-sair">

        <div>

          <h2>Sair da conta</h2>

          <p>
            Você poderá entrar novamente quando quiser.
          </p>

        </div>

        <button
          class="btn-sair"
          @click="sair"
        >
          Sair
        </button>

      </section>

    </main>


    <div class="patinhas">

      <span class="pata-grande">
        🐾
      </span>

      <span class="pata-pequena">
        🐾
      </span>

    </div>


    <footer>

      <span class="footer-pata">
        🐾
      </span>

      <strong>PetHope</strong>

      <span>·</span>

      <span>
        Fazendo a diferença na vida dos animais.
      </span>

    </footer>

  </div>
</template>


<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const router = useRouter()

const tipoSessao = ref('')

const dados = ref({
  nome: '',
  tipo_usuario: null,
  endereco: '',
  contato: '',
  foto: ''
})


const textoTipo = computed(() => {

  if (tipoSessao.value === 'ong') {
    return 'ONG'
  }

  if (dados.value.tipo_usuario === 'voluntario') {
    return 'Voluntário'
  }

  return 'Adotante'

})


function urlFoto(caminho) {

  if (!caminho) {
    return ''
  }

  if (caminho.startsWith('http')) {
    return caminho
  }

  const baseURL =
    http.defaults.baseURL || 'http://localhost:8000'

  return `${baseURL}${caminho}`

}

async function selecionarFoto(event) {
  const arquivo = event.target.files[0]

  if (!arquivo) {
    return
  }

  const formData = new FormData()
  formData.append('arquivo', arquivo)

  try {
    const { data } = await http.post(
      '/api/perfil/foto',
      formData
    )

    dados.value.foto = data.foto

    console.log('Foto atualizada com sucesso:', data.foto)
  } catch (erro) {
    console.error('Erro ao enviar foto:', erro)

    alert(
      erro.response?.data?.detail ||
      'Não foi possível atualizar a foto.'
    )
  }
}

async function carregar() {

  try {

    const { data } =
      await http.get('/api/auth/me')

    console.log('DADOS DO PERFIL:', data)

    if (!data.autenticado) {

      router.push('/login')

      return

    }

    tipoSessao.value =
      data.tipo_sessao || ''

    dados.value.nome =
      data.nome || ''

    dados.value.tipo_usuario =
      data.tipo_usuario || null

    dados.value.endereco =
      data.endereco || ''

    dados.value.contato =
      data.contato || ''

    dados.value.foto =
      data.foto || ''

  } catch (erro) {

    console.error(
      'Erro ao carregar perfil:',
      erro
    )

    router.push('/login')

  }

}


async function sair() {

  try {

    await http.post(
      '/api/auth/logout'
    )

  } catch (erro) {

    console.error(
      'Erro ao sair:',
      erro
    )

  }

  router.push('/')

}


onMounted(carregar)
</script>


<style scoped src="../styles/perfil.css"></style>