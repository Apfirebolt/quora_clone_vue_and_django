import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { mountWithDependencies, mockComment } from '@/test/helpers'
import CommentForm from '@/components/CommentForm.vue'

describe('CommentForm.vue', () => {
  let wrapper
  let mockAxios

  beforeEach(() => {
    mockAxios = {
      post: vi.fn().mockResolvedValue({ data: mockComment }),
    }

    const mountOptions = mountWithDependencies(CommentForm, {
      props: {
        answerId: 'test-answer-uuid',
        closeModal: vi.fn(),
      },
      global: {
        mocks: {
          $axios: mockAxios,
        },
      },
    })
    wrapper = mount(CommentForm, mountOptions)
  })

  it('renders comment input field', () => {
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
    await textarea.setValue('This is a test comment')
    expect(textarea.element.value).toBe('This is a test comment')
  })
})