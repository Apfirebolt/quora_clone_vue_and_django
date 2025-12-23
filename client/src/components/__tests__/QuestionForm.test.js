import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { mountWithDependencies } from '@/test/helpers'
import QuestionForm from '@/components/QuestionForm.vue'

describe('QuestionForm.vue', () => {
  let wrapper
  let mockAxios

  beforeEach(() => {
    // Mock axios
    mockAxios = {
      post: vi.fn().mockResolvedValue({ data: { success: true } }),
      get: vi.fn().mockResolvedValue({ data: { results: [] } }),
    }

    const mountOptions = mountWithDependencies(QuestionForm, {
      props: {
        addQuestion: vi.fn(),
        updateQuestion: vi.fn(),
        closeModal: vi.fn(),
      },
      global: {
        mocks: {
          $axios: mockAxios,
        },
      },
    })
    wrapper = mount(QuestionForm, mountOptions)
  })

  it('renders the form elements', () => {
    expect(wrapper.find('input[type="text"]').exists()).toBe(true)
    expect(wrapper.find('textarea').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('renders without crashing', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('has form elements', () => {
    expect(wrapper.find('form').exists()).toBe(true)
  })

  it('can type in form fields', async () => {
    const titleInput = wrapper.find('input[type="text"]')
    const descriptionTextarea = wrapper.find('textarea')
    
    await titleInput.setValue('Test Question')
    await descriptionTextarea.setValue('Test description')
    
    expect(titleInput.element.value).toBe('Test Question')
    expect(descriptionTextarea.element.value).toBe('Test description')
  })
})