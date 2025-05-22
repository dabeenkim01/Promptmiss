import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PromptListView from '../views/PromptListView.vue'
import PromptCreateView from '../views/PromptCreateView.vue'
import PromptDetailView from '../views/PromptDetailView.vue'
import PromptUpdateView from '@/views/PromptUpdateView.vue'
import LoginView from '../views/LoginView.vue'
import SignupView from '../views/SignupView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView,
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
      path: '/prompts/:id/update',
      name: 'prompt-update',
      component: PromptUpdateView,
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
    {
      path: '/users/:id',
      name: 'user-profile',
      component: () => import('@/views/UserProfileView.vue')
    },
  ],
})

export default router
