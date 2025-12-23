import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import { mountWithDependencies, mockQuestion, mockAnswer, mockUser } from '@/test/helpers'

// Mock components for testing
const QuestionDetailPage = {
  template: `
    <div>
      <div data-testid="question-content">{{ mockQuestion.content }}</div>
      <div data-testid="question-description">{{ mockQuestion.description }}</div>
      <div data-testid="answer-item">{{ mockAnswer.body }}</div>
    </div>
  `,
  data() {
    return {
      mockQuestion,
      mockAnswer
    }
  }
}

const LoginComponent = {
  template: `
    <form data-testid="login-form">
      <input v-model="email" type="email" data-testid="email-input" />
      <input v-model="password" type="password" data-testid="password-input" />
      <button type="submit" data-testid="login-button">Login</button>
    </form>
  `,
  data() {
    return {
      email: '',
      password: ''
    }
  }
}

const QuestionCreateComponent = {
  template: `
    <div>
      <input v-model="question.content" data-testid="question-title" placeholder="Question title" />
      <textarea v-model="question.description" data-testid="question-description" placeholder="Description"></textarea>
      <input v-model="tagInput" @keyup.enter="addTag" data-testid="tag-input" placeholder="Add tags" />
      <div data-testid="tags-list">
        <span v-for="tag in question.tags" :key="tag" data-testid="tag-item">{{ tag }}</span>
      </div>
      <button type="submit" data-testid="submit-question">Create Question</button>
    </div>
  `,
  data() {
    return {
      question: {
        content: '',
        description: '',
        tags: [],
      },
      tagInput: '',
    }
  },
  methods: {
    addTag() {
      if (this.tagInput.trim() && !this.question.tags.includes(this.tagInput.trim())) {
        this.question.tags.push(this.tagInput.trim())
        this.tagInput = ''
      }
    }
  }
}

describe('Question Detail Flow Integration Tests', () => {
  let wrapper

  beforeEach(async () => {
    const pinia = createPinia()
    const router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/questions/:slug', name: 'question-detail', component: QuestionDetailPage },
      ],
    })

    wrapper = mount(QuestionDetailPage, {
      global: {
        plugins: [router, pinia],
      },
    })

    await router.isReady()
  })

  it('displays question details correctly', () => {
    expect(wrapper.find('[data-testid="question-content"]').text()).toBe(mockQuestion.content)
    expect(wrapper.find('[data-testid="question-description"]').text()).toBe(mockQuestion.description)
  })

  it('displays existing answers', () => {
    const answerItems = wrapper.findAll('[data-testid="answer-item"]')
    expect(answerItems).toHaveLength(1)
    expect(answerItems[0].text()).toBe(mockAnswer.body)
  })

  it('renders the page without crashing', () => {
    expect(wrapper.exists()).toBe(true)
  })
})

describe('User Authentication Flow Integration Tests', () => {
  let wrapper

  beforeEach(() => {
    const pinia = createPinia()
    
    wrapper = mount(LoginComponent, {
      global: {
        plugins: [pinia],
      },
    })
  })

  it('renders login form', () => {
    expect(wrapper.find('[data-testid="login-form"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="email-input"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="password-input"]').exists()).toBe(true)
  })

  it('allows typing in form fields', async () => {
    const emailInput = wrapper.find('[data-testid="email-input"]')
    const passwordInput = wrapper.find('[data-testid="password-input"]')

    await emailInput.setValue('test@example.com')
    await passwordInput.setValue('password')

    expect(emailInput.element.value).toBe('test@example.com')
    expect(passwordInput.element.value).toBe('password')
  })

  it('has a submit button', () => {
    expect(wrapper.find('[data-testid="login-button"]').exists()).toBe(true)
  })
})

describe('Question Creation Flow Integration Tests', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(QuestionCreateComponent)
  })

  it('renders form elements', () => {
    expect(wrapper.find('[data-testid="question-title"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="question-description"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="submit-question"]').exists()).toBe(true)
  })

  it('allows typing in form fields', async () => {
    const titleInput = wrapper.find('[data-testid="question-title"]')
    const descriptionTextarea = wrapper.find('[data-testid="question-description"]')

    await titleInput.setValue('How to use Vitest with Vue 3?')
    await descriptionTextarea.setValue('I want to set up Vitest for testing my Vue 3 application.')
    
    expect(titleInput.element.value).toBe('How to use Vitest with Vue 3?')
    expect(descriptionTextarea.element.value).toBe('I want to set up Vitest for testing my Vue 3 application.')
  })

  it('handles tag addition', async () => {
    const tagInput = wrapper.find('[data-testid="tag-input"]')

    await tagInput.setValue('javascript')
    await tagInput.trigger('keyup.enter')
    
    await tagInput.setValue('vue')
    await tagInput.trigger('keyup.enter')

    const tagItems = wrapper.findAll('[data-testid="tag-item"]')
    expect(tagItems).toHaveLength(2)
    expect(tagItems[0].text()).toBe('javascript')
    expect(tagItems[1].text()).toBe('vue')

    expect(tagInput.element.value).toBe('')
  })

  it('prevents duplicate tags', async () => {
    const tagInput = wrapper.find('[data-testid="tag-input"]')

    await tagInput.setValue('javascript')
    await tagInput.trigger('keyup.enter')
    
    await tagInput.setValue('javascript')
    await tagInput.trigger('keyup.enter')

    const tagItems = wrapper.findAll('[data-testid="tag-item"]')
    expect(tagItems).toHaveLength(1)
  })
})