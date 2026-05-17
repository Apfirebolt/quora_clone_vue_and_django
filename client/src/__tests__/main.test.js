import { describe, it, expect, beforeEach, vi } from 'vitest'

const mountMock = vi.fn()
const useMock = vi.fn()
const componentMock = vi.fn()
const createAppMock = vi.fn(() => ({ use: useMock, component: componentMock, mount: mountMock }))
const createPiniaMock = vi.fn(() => 'pinia')
const swiperUseMock = vi.fn()

vi.mock('vue', () => ({ createApp: createAppMock }))
vi.mock('pinia', () => ({ createPinia: createPiniaMock }))
vi.mock('vue3-smooth-scroll', () => ({ default: 'VueSmoothScroll' }))
vi.mock('vue-toastification', () => ({ default: 'Toast' }))
vi.mock('vue-awesome-swiper', () => ({ default: 'VueAwesomeSwiper' }))
vi.mock('@/routes', () => ({ default: 'router' }))
vi.mock('@/App.vue', () => ({ default: 'App' }))
vi.mock('@/components/HeaderComponent.vue', () => ({ default: 'HeaderComponent' }))
vi.mock('@/components/FooterComponent.vue', () => ({ default: 'FooterComponent' }))
vi.mock('swiper', () => ({ default: { use: swiperUseMock }, Pagination: 'pagination' }))
vi.mock('swiper/css', () => ({}))
vi.mock('swiper/css/pagination', () => ({}))
vi.mock('aos/dist/aos.css', () => ({}))
vi.mock('@/style.css', () => ({}))

describe('Main application bootstrap', () => {
  beforeEach(() => {
    vi.resetModules()
    vi.clearAllMocks()
  })

  it('initializes Vue app with router, pinia, plugins, and mounts to #app', async () => {
    await import('@/main.js')

    expect(createAppMock).toHaveBeenCalledWith('App')
    expect(useMock).toHaveBeenNthCalledWith(1, 'router')
    expect(useMock).toHaveBeenNthCalledWith(2, 'pinia')
    expect(useMock).toHaveBeenNthCalledWith(3, 'VueSmoothScroll')
    expect(useMock).toHaveBeenNthCalledWith(4, 'VueAwesomeSwiper')
    expect(useMock).toHaveBeenNthCalledWith(5, 'Toast', expect.any(Object))
    expect(componentMock).toHaveBeenCalledWith('header-component', 'HeaderComponent')
    expect(componentMock).toHaveBeenCalledWith('footer-component', 'FooterComponent')
    expect(mountMock).toHaveBeenCalledWith('#app')
    expect(swiperUseMock).toHaveBeenCalledWith(['pagination'])
  })
})
