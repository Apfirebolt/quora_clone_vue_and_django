import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { mountWithDependencies, mockQuestion } from '@/test/helpers'
import QuestionCard from '@/components/QuestionCard.vue'

// Mock dayjs
vi.mock('dayjs', () => ({
  default: () => ({
    fromNow: () => '2 hours ago',
    format: () => '2023-01-01',
  }),
}))

describe('QuestionCard.vue', () => {
  let wrapper

  beforeEach(() => {
    const mountOptions = mountWithDependencies(QuestionCard, {
      props: {
        question: mockQuestion,
        deleteQuestion: vi.fn(),
        updateQuestion: vi.fn(),
        viewQuestion: vi.fn(),
        isQuestionOwner: () => false,
      },
    })
    wrapper = mount(QuestionCard, mountOptions)
  })

  it('renders question content', () => {
    expect(wrapper.text()).toContain(mockQuestion.content)
  })

  it('renders question description', () => {
    expect(wrapper.text()).toContain(mockQuestion.description)
  })

  it('displays author information', () => {
    expect(wrapper.text()).toContain(mockQuestion.author.username)
  })

  it('renders the component', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('has clickable buttons', () => {
    const buttons = wrapper.findAll('button')
    expect(buttons.length).toBeGreaterThan(0)
  })
})