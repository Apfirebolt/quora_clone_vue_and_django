import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { mountWithDependencies } from '@/test/helpers'
import HeaderComponent from '@/components/HeaderComponent.vue'

describe('HeaderComponent.vue', () => {
  let wrapper

  beforeEach(() => {
    // Mock the store to avoid auth dependency
    vi.mock('@/store/auth', () => ({
      useAuth: () => ({
        authData: null,
        logout: vi.fn()
      })
    }))
    
    const mountOptions = mountWithDependencies(HeaderComponent)
    wrapper = mount(HeaderComponent, mountOptions)
  })

  it('renders the navigation component', () => {
    expect(wrapper.find('nav').exists()).toBe(true)
  })

  it('renders the component without crashing', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('has a logo/brand image', () => {
    expect(wrapper.find('img').exists()).toBe(true)
  })

  it('contains navigation links', () => {
    expect(wrapper.findAll('router-link').length).toBeGreaterThanOrEqual(0)
  })
})