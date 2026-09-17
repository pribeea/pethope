import { createRouter, createWebHistory } from 'vue-router'
import http from '../api/http'

import Home from '../views/Home.vue'
import Cadastro from '../views/Cadastro.vue'
import OpcoesLogin from '../views/OpcoesLogin.vue'
import Login from '../views/Login.vue'
import CadastroOng from '../views/CadastroOng.vue'
import LoginOng from '../views/LoginOng.vue'
import ListaOngs from '../views/Listaongs.vue'
import AnimaisPorOng from '../views/Animaisporong.vue'
import CadastroAnimal from '../views/CadastroAnimal.vue'
import ListaAnimais from '../views/ListaAnimais.vue'
import AnimalDetalhes from '../views/AnimalDetalhes.vue'
import EditarAnimal from '../views/EditarAnimal.vue'
import FormularioAdocao from '../views/FormularioAdocao.vue'
import MinhasAdocoes from '../views/MinhasAdocoes.vue'
import Solicitacoes from '../views/Solicitacoes.vue'
import DashboardAdotante from '../views/DashboardAdotante.vue'
import DashboardVoluntario from '../views/DashboardVoluntario.vue'
import DashboardOng from '../views/DashboardOng.vue'
import MuralAtividades from '../views/MuralAtividades.vue'
import CadastroAtividade from '../views/CadastroAtividade.vue'
import FormularioVoluntario from '../views/FormularioVoluntario.vue'
import InscricoesAtividade from '../views/InscricoesAtividade.vue'
import MinhasAtividadesOng from '../views/MinhasAtividadesOng.vue'
import MinhasAtividadesVoluntario from '../views/MinhasAtividadesVoluntario.vue'
import AtividadeDetalhe from '../views/AtividadeDetalhe.vue'
import Doacoes from '../views/Doacoes.vue'
import FormularioDoacao from '../views/FormularioDoacao.vue'
import PagamentoDoacao from '../views/PagamentoDoacao.vue'
import MinhasDoacoes from '../views/MinhasDoacoes.vue'
import DoacoesRecebidas from '../views/DoacoesRecebidas.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/cadastro', name: 'cadastro', component: Cadastro },
  { path: '/opcoes_login', name: 'opcoes_login', component: OpcoesLogin },
  { path: '/login', name: 'login', component: Login },
  { path: '/cadastro_ong', name: 'cadastro_ong', component: CadastroOng },
  { path: '/login_ong', name: 'login_ong', component: LoginOng },

  { path: '/dashboard_adotante', name: 'dashboard_adotante', component: DashboardAdotante, meta: { roles: ['usuario'] } },
  { path: '/dashboard_voluntario', name: 'dashboard_voluntario', component: DashboardVoluntario, meta: { roles: ['usuario'] } },
  { path: '/dashboard_ong', name: 'dashboard_ong', component: DashboardOng, meta: { roles: ['ong'] } },

  { path: '/ongs', name: 'ongs', component: ListaOngs, meta: { roles: ['usuario'] } },
  { path: '/ongs/:ongId/animais', name: 'animais_por_ong', component: AnimaisPorOng, props: true, meta: { roles: ['usuario'] } },
  { path: '/animais', name: 'animais', component: ListaAnimais, meta: { roles: ['ong'] } },
  { path: '/cadastro_animal', name: 'cadastro_animal', component: CadastroAnimal, meta: { roles: ['ong'] } },
  { path: '/animal/:id', name: 'animal_detalhes', component: AnimalDetalhes, props: true, meta: { roles: ['usuario', 'ong'] } },
  { path: '/editar_animal/:id', name: 'editar_animal', component: EditarAnimal, props: true, meta: { roles: ['ong'] } },

  // A listagem geral de animais deixou de ser uma etapa de adoção do usuário.
  // O caminho antigo é mantido apenas para compatibilidade e leva às ONGs.
  { path: '/adocao', name: 'adocao', redirect: '/ongs', meta: { roles: ['usuario'] } },
  { path: '/adotar/:id', name: 'formulario_adocao', component: FormularioAdocao, props: true, meta: { roles: ['usuario'] } },
  { path: '/minhas_adocoes', name: 'minhas_adocoes', component: MinhasAdocoes, meta: { roles: ['usuario'] } },
  { path: '/solicitacoes', name: 'solicitacoes', component: Solicitacoes, meta: { roles: ['ong'] } },

  { path: '/atividades', name: 'atividades', component: MuralAtividades, meta: { roles: ['usuario'] } },
  { path: '/cadastrar-atividade', name: 'cadastrar_atividade', component: CadastroAtividade, meta: { roles: ['ong'] } },
  { path: '/formulario-voluntario/:atividadeId', name: 'formulario_voluntario', component: FormularioVoluntario, props: true, meta: { roles: ['usuario'] } },
  { path: '/atividades/:atividadeId/inscricoes', name: 'inscricoes_atividade', component: InscricoesAtividade, props: true, meta: { roles: ['ong'] } },
  { path: '/atividades-ong', name: 'atividades_ong', component: MinhasAtividadesOng, meta: { roles: ['ong'] } },
  { path: '/minhas-atividades-voluntario', name: 'minhas_atividades_voluntario', component: MinhasAtividadesVoluntario, meta: { roles: ['usuario'] } },
  { path: '/atividades/:atividadeId', name: 'detalhes_atividade', component: AtividadeDetalhe, props: true, meta: { roles: ['usuario', 'ong'] } },

  { path: '/doacoes', name: 'doacoes', component: Doacoes, meta: { roles: ['usuario'] } },
  { path: '/doar/:ongId', name: 'formulario_doacao', component: FormularioDoacao, props: true, meta: { roles: ['usuario'] } },
  { path: '/doacao/:id/pagamento', name: 'pagamento_doacao', component: PagamentoDoacao, props: true, meta: { roles: ['usuario'] } },
  { path: '/minhas-doacoes', name: 'minhas_doacoes', component: MinhasDoacoes, meta: { roles: ['usuario'] } },
  { path: '/doacoes-recebidas', name: 'doacoes_recebidas', component: DoacoesRecebidas, meta: { roles: ['ong'] } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  if (!to.meta.roles) {
    return true
  }

  try {
    const { data } = await http.get('/api/auth/me')

    if (!data.autenticado) {
      return data.tipo_sessao === 'ong' ? '/login_ong' : '/login'
    }

    const sessao = data.tipo_sessao

    if (to.meta.roles.includes(sessao)) {
      return true
    }

    if (sessao === 'ong') {
      return '/dashboard_ong'
    }

    if (data.tipo_usuario === 'voluntario') {
      return '/dashboard_voluntario'
    }

    return '/dashboard_adotante'
  } catch {
    return '/login'
  }
})

export default router
