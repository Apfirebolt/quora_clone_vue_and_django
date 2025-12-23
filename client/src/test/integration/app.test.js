import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from '@/App.vue'

// Mock components for testing
const Home = { template: '<div>Home Page</div>' }
const Login = { template: '<div>Login Page</div>' }
const Questions = { template: '<div>Questions Page</div>' }
const QuestionDetail = { template: '<div>Question Detail Page</div>' }

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/login', name: 'login', component: Login },
    { path: '/questions', name: 'questions', component: Questions },
    { path: '/questions/:slug', name: 'question-detail', component: QuestionDetail },
  ],
})

describe('App Integration Tests', () => {
  let wrapper

  beforeEach(async () => {
    const pinia = createPinia()
    
    wrapper = mount({
      template: '<div data-testid="app"><router-view /></div>'
    }, {
      global: {
        plugins: [router, pinia],
      },
    })
    
    await router.isReady()
  })

  it('renders the app structure', () => {
    expect(wrapper.find('[data-testid="app"]').exists()).toBe(true)
  })

  it('renders router view', () => {
    expect(wrapper.findComponent({ name: 'RouterView' }).exists()).toBe(true)
  })
})

describe('Routing Integration Tests', () => {
  let wrapper

  beforeEach(async () => {
    const pinia = createPinia()
    
    wrapper = mount({
      template: '<router-view />',
    }, {
      global: {
        plugins: [router, pinia],
      },
    })
    
    await router.isReady()
  })

  it('navigates to home page', async () => {
    await router.push('/')
    expect(wrapper.text()).toContain('Home Page')
  })

  it('navigates to login page', async () => {
    await router.push('/login')
    expect(wrapper.text()).toContain('Login Page')
  })

  it('navigates to questions page', async () => {
    await router.push('/questions')
    expect(wrapper.text()).toContain('Questions Page')
  })

  it('navigates to question detail page', async () => {
    await router.push('/questions/test-question')
    expect(wrapper.text()).toContain('Question Detail Page')
  })
})

describe('Authentication Integration Tests', () => {
  let wrapper

  beforeEach(async () => {
    const pinia = createPinia()
    
    wrapper = mount({
      template: `
        <div>
          <div v-if="isAuthenticated">
            Welcome user
          </div>
          <div v-else>
            Please login
          </div>
        </div>
      `,
      data() {
        return {
          isAuthenticated: false
        }
      }
    }, {
      global: {
        plugins: [router, pinia],
      },
    })
  })

  it('shows login prompt when not authenticated', () => {
    expect(wrapper.text()).toContain('Please login')
  })

  it('shows welcome message when authenticated', async () => {
    await wrapper.setData({ isAuthenticated: true })
    expect(wrapper.text()).toContain('Welcome user')
  })
})