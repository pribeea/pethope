<template>
  <div class="page-dashboard">

    <!-- NAVBAR -->
    <header class="navbar">

      <h2 class="logo">
        <img
          src="/pata-branca.png"
          class="logo-pata"
          alt=""
        />
        PetHope
      </h2>

      <nav class="menu">
        <router-link to="/dashboard_adotante">
          Início
        </router-link>

        <router-link :to="{ name: 'ongs' }">
          Adotar
        </router-link>

        <router-link to="/minhas_adocoes">
          Minhas adoções
        </router-link>

        <router-link to="/doacoes">
          Doações
        </router-link>

        <router-link to="/perfil">
          Perfil
        </router-link>

        <a href="#" @click.prevent="sair">
          Sair
        </a>
      </nav>

    </header>


    <!-- CONTEÚDO -->
    <main class="dashboard-container">

      <!-- BOAS-VINDAS -->
      <section class="welcome-section">

        <div class="welcome-text">

          <p class="welcome-small">
            Seja bem-vindo ao PetHope! 🐾
          </p>

          <h1>
            Olá, {{ nome }}!
          </h1>

          <p class="welcome-description">
            Que tal encontrar um novo companheiro para
            fazer parte da sua história?
          </p>

          <router-link
            :to="{ name: 'ongs' }"
            class="btn-primary"
          >
            Encontrar meu pet
          </router-link>

        </div>


        <!-- ARTE -->
        <div class="welcome-art">

          <div class="art-circle"></div>

          <span class="paw paw-1">🐾</span>
          <span class="paw paw-2">🐾</span>
          <span class="paw paw-3">🐾</span>

          <div class="art-heart">
            ♡
          </div>

        </div>

      </section>


      <!-- AÇÕES -->
      <section class="actions-section">

        <div class="section-title">

          <h2>
            O que você quer fazer?
          </h2>

          <p>
            Acesse rapidamente as principais opções.
          </p>

        </div>


        <div class="cards-grid">


          <!-- ADOTAR -->
          <div class="action-card destaque">

            <div class="card-icon">
              🐶
            </div>

            <div class="card-content">

              <h3>
                Encontrar um pet
              </h3>

              <p>
                Conheça nossas ONGs parceiras e encontre
                um animal esperando por um lar.
              </p>

              <router-link
                :to="{ name: 'ongs' }"
                class="card-link"
              >
                Ver ONGs →
              </router-link>

            </div>

          </div>


          <!-- ADOÇÕES -->
          <div class="action-card">

            <div class="card-icon">
              ❤️
            </div>

            <div class="card-content">

              <h3>
                Minhas adoções
              </h3>

              <p>
                Acompanhe suas solicitações e veja
                o andamento das suas adoções.
              </p>

              <router-link
                to="/minhas_adocoes"
                class="card-link"
              >
                Ver minhas adoções →
              </router-link>

            </div>

          </div>


          <!-- DOAÇÃO -->
          <div class="action-card">

            <div class="card-icon">
              💜
            </div>

            <div class="card-content">

              <h3>
                Fazer uma doação
              </h3>

              <p>
                Ajude uma ONG parceira a continuar
                cuidando dos animais.
              </p>

              <router-link
                to="/doacoes"
                class="card-link"
              >
                Doar agora →
              </router-link>

            </div>

          </div>


          <!-- HISTÓRICO -->
          <div class="action-card">

            <div class="card-icon">
              📋
            </div>

            <div class="card-content">

              <h3>
                Minhas doações
              </h3>

              <p>
                Consulte o histórico das doações
                que você já realizou.
              </p>

              <router-link
                to="/minhas-doacoes"
                class="card-link"
              >
                Ver histórico →
              </router-link>

            </div>

          </div>

        </div>

      </section>


      <!-- FRASE FINAL -->
      <section class="bottom-message">

        <div class="bottom-paw">
          🐾
        </div>

        <div>
          <h3>
            Pequenos gestos fazem grandes diferenças.
          </h3>

          <p>
            Cada adoção e cada doação ajudam a transformar
            a vida de um animal.
          </p>
        </div>

      </section>

    </main>

  </div>
</template>


<script setup>

import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const router = useRouter()

const nome = ref('')


async function carregar() {

  try {

    const { data } =
      await http.get('/api/auth/me')


    /*
     * Verifica se existe usuário logado
     */
    if (
      !data.autenticado ||
      data.tipo_sessao !== 'usuario'
    ) {

      router.push('/login')

      return

    }


    /*
     * Apenas adotante pode acessar
     */
    if (
      data.tipo_usuario !== 'adotante'
    ) {

      if (
        data.tipo_usuario === 'voluntario'
      ) {

        router.push('/dashboard_voluntario')

      } else {

        router.push('/login')

      }

      return

    }


    /*
     * Nome do usuário
     */
    nome.value = data.nome

  } catch (err) {

    console.error(
      'Erro ao carregar dashboard:',
      err
    )

    router.push('/login')

  }

}


/*
 * Logout
 */
async function sair() {

  try {

    await http.post(
      '/api/auth/logout'
    )

    router.push('/')

  } catch (err) {

    console.error(
      'Erro ao fazer logout:',
      err
    )

  }
}
onMounted(carregar)

</script>

<style scoped src="../styles/dashboard.css"></style>
