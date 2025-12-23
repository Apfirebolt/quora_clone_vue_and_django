import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'

// Mock router for testing
export function createMockRouter() {
  return createRouter({
    history: createWebHistory(),
    routes: [
      { path: '/', name: 'Home', component: { template: '<div>Home</div>' } },
      { path: '/login', name: 'Login', component: { template: '<div>Login</div>' } },
      { path: '/register', name: 'Register', component: { template: '<div>Register</div>' } },
      { path: '/dashboard', name: 'Dashboard', component: { template: '<div>Dashboard</div>' } },
      { path: '/profile', name: 'Profile', component: { template: '<div>Profile</div>' } },
      { path: '/users', name: 'Users', component: { template: '<div>Users</div>' } },
      { path: '/my-questions', name: 'MyQuestions', component: { template: '<div>My Questions</div>' } },
      { path: '/my-answers', name: 'MyAnswers', component: { template: '<div>My Answers</div>' } },
      { path: '/questions', name: 'questions', component: { template: '<div>Questions</div>' } },
      { path: '/questions/:slug', name: 'question-detail', component: { template: '<div>Question Detail</div>' } },
    ],
  })
}

// Mock store for testing
export function createMockStore() {
  return createPinia()
}

// Common test data
export const mockUser = {
  id: 1,
  username: 'testuser',
  email: 'test@example.com',
  firstName: 'Test',
  lastName: 'User',
  profilePicture: null,
}

export const mockQuestion = {
  id: 1,
  uuid: '123e4567-e89b-12d3-a456-426614174000',
  slug: 'test-question',
  content: 'This is a test question?',
  description: 'A detailed description of the test question',
  author: mockUser,
  upvotes: [],
  downvotes: [],
  tags: [
    { id: 1, name: 'javascript' },
    { id: 2, name: 'vue' }
  ],
  created_at: '2023-01-01T00:00:00Z',
  updated_at: '2023-01-01T00:00:00Z',
}

export const mockAnswer = {
  id: 1,
  uuid: '123e4567-e89b-12d3-a456-426614174001',
  body: 'This is a test answer.',
  author: mockUser,
  question: mockQuestion,
  upvotes: [],
  downvotes: [],
  created_at: '2023-01-01T01:00:00Z',
  updated_at: '2023-01-01T01:00:00Z',
}

export const mockComment = {
  id: 1,
  uuid: '123e4567-e89b-12d3-a456-426614174002',
  body: 'This is a test comment.',
  author: mockUser,
  answer: mockAnswer,
  created_at: '2023-01-01T02:00:00Z',
  updated_at: '2023-01-01T02:00:00Z',
}

// Helper to mount components with common dependencies
export function mountWithDependencies(component, options = {}) {
  const router = createMockRouter()
  const pinia = createMockStore()
  
  return {
    router,
    pinia,
    global: {
      plugins: [router, pinia],
      ...options.global,
    },
    ...options,
  }
}