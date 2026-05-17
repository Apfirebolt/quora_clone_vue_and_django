import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

localStorage.getItem = vi.fn(() => null)

const toastSuccess = vi.fn()
const toastError = vi.fn()
const routerPush = vi.fn()
const httpClientMock = {
  post: vi.fn(),
  get: vi.fn(),
  put: vi.fn(),
  delete: vi.fn(),
}

vi.mock('vue-toastification', () => ({
  useToast: () => ({ success: toastSuccess, error: toastError }),
}))

vi.mock('@/routes', () => ({
  default: {
    push: routerPush,
  },
}))

vi.mock('@/plugins/interceptor', () => ({
  default: httpClientMock,
}))

const { useAuth } = await import('@/store/auth')

describe('Auth Store', () => {
  let authStore

  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    localStorage.clear()
    authStore = useAuth()
  })

  it('logs in successfully and stores user data', async () => {
    const payload = { email: 'test@example.com', password: 'password' }
    const responseData = { access: 'fake-access', refresh: 'fake-refresh' }
    httpClientMock.post.mockResolvedValue({ data: responseData })

    await authStore.loginAction(payload)

    expect(httpClientMock.post).toHaveBeenCalledWith('login', payload)
    expect(authStore.authData).toEqual(responseData)
    expect(localStorage.setItem).toHaveBeenCalledWith('user', JSON.stringify(responseData))
    expect(toastSuccess).toHaveBeenCalledWith('Login successful!')
    expect(routerPush).toHaveBeenCalledWith('/dashboard')
  })

  it('returns error when login fails', async () => {
    const payload = { email: 'test@example.com', password: 'wrong' }
    const error = new Error('Login failed')
    httpClientMock.post.mockRejectedValue(error)

    let result
    try {
      result = await authStore.loginAction(payload)
    } catch (catchError) {
      result = catchError
    }

    expect(result).toBe(error)
    expect(authStore.authData).toBeNull()
    expect(toastSuccess).not.toHaveBeenCalled()
  })

  it('registers successfully and shows success toast', async () => {
    const payload = { email: 'new@example.com', password: 'password' }
    const responseData = { access: 'fake-access', refresh: 'fake-refresh' }
    httpClientMock.post.mockResolvedValue({ data: responseData })

    await authStore.registerAction(payload)

    expect(httpClientMock.post).toHaveBeenCalledWith('register', payload)
    expect(authStore.authData).toEqual(responseData)
    expect(toastSuccess).toHaveBeenCalledWith('Registration successful!')
    expect(routerPush).toHaveBeenCalledWith('/dashboard')
  })

  it('shows field error messages on registration validation failure', async () => {
    const payload = { email: 'bad' }
    const error = {
      response: {
        status: 400,
        data: {
          email: ['Invalid email address'],
          password: ['Password too short'],
        },
      },
    }
    httpClientMock.post.mockRejectedValue(error)

    let result
    try {
      result = await authStore.registerAction(payload)
    } catch (catchError) {
      result = catchError
    }

    expect(result).toBe(error)
    expect(toastError).toHaveBeenCalledWith('email: Invalid email address')
    expect(toastError).toHaveBeenCalledWith('password: Password too short')
  })

  it('fetches profile data and toggles loading correctly', async () => {
    authStore.authData = { access: 'fake-access' }
    httpClientMock.get.mockResolvedValue({ data: { name: 'Tester' } })

    await authStore.getProfileDataAction()

    expect(httpClientMock.get).toHaveBeenCalledWith('profile', { headers: { Authorization: 'Bearer fake-access' } })
    expect(authStore.profileData).toEqual({ name: 'Tester' })
    expect(authStore.loading).toBe(false)
  })

  it('returns error when profile fetch fails', async () => {
    authStore.authData = { access: 'fake-access' }
    const error = new Error('Network error')
    httpClientMock.get.mockRejectedValue(error)

    let result
    try {
      result = await authStore.getProfileDataAction()
    } catch (catchError) {
      result = catchError
    }

    expect(result).toBe(error)
    expect(authStore.loading).toBe(false)
  })

  it('logs out and clears auth state', () => {
    authStore.authData = { access: 'fake-access' }
    localStorage.setItem('user', JSON.stringify({ access: 'fake-access' }))

    authStore.logout()

    expect(authStore.authData).toBeNull()
    expect(localStorage.getItem('user')).toBeNull()
    expect(routerPush).toHaveBeenCalledWith('/login')
    expect(toastSuccess).toHaveBeenCalledWith('Logout successful!')
  })
})