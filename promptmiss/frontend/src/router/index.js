import { createRouter, createWebHistory } from 'vue-router'
import PromptListView from '../views/PromptListView.vue'
import PromptCreateView from '../views/PromptCreateView.vue'
import PromptDetailView from '../views/PromptDetailView.vue'
import LoginView from '../views/LoginView.vue'
import SignupView from '../views/SignupView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: PromptListView,
    },
    {
      path: '/prompts',
      name: 'prompts',
      component: PromptListView,
    },
    {
      path: '/prompts/create',
      name: 'prompt-create',
      component: PromptCreateView,
    },
    {
      path: '/prompts/:id',
      name: 'prompt-detail',
      component: PromptDetailView,
    },
    {
      path: '/prompts/:id/edit',
      name: 'prompt-edit',
      component: () => import('../views/PromptUpdateView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
  ],
})

export default router
