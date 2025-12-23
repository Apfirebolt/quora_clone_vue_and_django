import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { mountWithDependencies, mockAnswer } from '@/test/helpers'
import AnswerForm from '@/components/AnswerForm.vue'

describe('AnswerForm.vue', () => {
  let wrapper
  let mockAxios

  beforeEach(() => {
    mockAxios = {
      post: vi.fn().mockResolvedValue({ data: { success: true } }),
    }

    const mountOptions = mountWithDependencies(AnswerForm, {
      props: {
        questionSlug: 'test-question',
        addAnswer: vi.fn(),
        updateAnswer: vi.fn(),
        closeModal: vi.fn(),
      },
      global: {
        mocks: {
          $axios: mockAxios,
        },
      },
    })
    wrapper = mount(AnswerForm, mountOptions)
  })

  it('renders textarea for answer input', () => {
    expect(wrapper.find('textarea').exists()).toBe(true)
  })

  it('renders submit button', () => {
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('renders without crashing', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('can type in textarea', async () => {
    const textarea = wrapper.find('textarea')
    await textarea.setValue('This is my answer')
    expect(textarea.element.value).toBe('This is my answer')
  })
})