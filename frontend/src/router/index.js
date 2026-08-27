import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Cadastro from '../views/Cadastro.vue'
import OpcoesLogin from '../views/OpcoesLogin.vue'
import Login from '../views/Login.vue'
import CadastroOng from '../views/CadastroOng.vue'
import LoginOng from '../views/LoginOng.vue'
import ListaOngs from '../views/ListaOngs.vue'
import AnimaisPorOng from '../views/AnimaisPorOng.vue'
import CadastroAnimal from '../views/CadastroAnimal.vue'
import ListaAnimais from '../views/ListaAnimais.vue'
import AnimalDetalhes from '../views/AnimalDetalhes.vue'
import EditarAnimal from '../views/EditarAnimal.vue'
import Adocao from '../views/Adocao.vue'
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


const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/cadastro', name: 'cadastro', component: Cadastro },
  { path: '/opcoes_login', name: 'opcoes_login', component: OpcoesLogin },
  { path: '/login', name: 'login', component: Login },
  { path: '/cadastro_ong', name: 'cadastro_ong', component: CadastroOng },
  { path: '/login_ong', name: 'login_ong', component: LoginOng },
  { path: '/ongs', name: 'ongs', component: ListaOngs },
  { path: '/ongs/:ongId/animais', name: 'animais_por_ong', component: AnimaisPorOng, props: true },
  { path: '/cadastro_animal', name: 'cadastro_animal', component: CadastroAnimal },
  { path: '/animais', name: 'animais', component: ListaAnimais },
  { path: '/animal/:id', name: 'animal_detalhes', component: AnimalDetalhes, props: true },
  { path: '/editar_animal/:id', name: 'editar_animal', component: EditarAnimal, props: true },
  { path: '/adocao', name: 'adocao', component: Adocao },
  { path: '/adotar/:id', name: 'formulario_adocao', component: FormularioAdocao, props: true },
  { path: '/minhas_adocoes', name: 'minhas_adocoes', component: MinhasAdocoes },
  { path: '/solicitacoes', name: 'solicitacoes', component: Solicitacoes },
  { path: '/dashboard_adotante', name: 'dashboard_adotante', component: DashboardAdotante },
  { path: '/dashboard_voluntario', name: 'dashboard_voluntario', component: DashboardVoluntario },
  { path: '/dashboard_ong', name: 'dashboard_ong', component: DashboardOng },
  { path: '/atividades', name: 'atividades', component: MuralAtividades },
  { path: '/cadastrar-atividade', name: 'cadastrar_atividade', component: CadastroAtividade },
  { path: '/formulario-voluntario/:atividadeId', name: 'formulario_voluntario', component: FormularioVoluntario, props: true },
  { path: '/atividades/:atividadeId/inscricoes', name: 'inscricoes_atividade', component: InscricoesAtividade, props: true },
  { path: '/atividades-ong', name: 'atividades_ong', component: MinhasAtividadesOng },
  { path: '/minhas-atividades-voluntario', name: 'minhas_atividades_voluntario', component: MinhasAtividadesVoluntario },
  { path: '/atividades/:atividadeId', name: 'detalhes_atividade', component: AtividadeDetalhe, props: true },
]


const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
