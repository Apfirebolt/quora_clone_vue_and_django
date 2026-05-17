import { describe, it, expect, beforeEach, vi } from 'vitest'

describe('Router configuration', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('exports the expected route names', async () => {
    const { default: router } = await import('@/routes')
    const routeNames = router.options.routes.map(route => route.name)

    expect(routeNames).toEqual(
      expect.arrayContaining([
        'Home',
        'Login',
        'Register',
        'Profile',
        'Dashboard',
        'MyQuestions',
        'MyAnswers',
        'QuestionDetail',
        'Users',
        'UserDetail',
        'ServerError',
        'NotFound',
      ])
    )
  })

  it('redirects to login when authGuard finds no user', async () => {
    const { default: router } = await import('@/routes')
    const profileRoute = router.options.routes.find(route => route.name === 'Profile')
    const next = vi.fn()
    localStorage.getItem = vi.fn(() => null)

    await profileRoute.beforeEnter({}, {}, next)

    expect(next).toHaveBeenCalledWith('/login')
  })

  it('allows navigation when authGuard finds a user', async () => {
    const { default: router } = await import('@/routes')
    const profileRoute = router.options.routes.find(route => route.name === 'Profile')
    const next = vi.fn()
    localStorage.getItem = vi.fn(() => JSON.stringify({ access: 'x' }))

    await profileRoute.beforeEnter({}, {}, next)

    expect(next).toHaveBeenCalledWith()
  })
})
