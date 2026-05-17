import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

const toastSuccess = vi.fn()
const httpClientMock = {
  get: vi.fn(),
  post: vi.fn(),
  delete: vi.fn(),
}

vi.mock('vue-toastification', () => ({
  useToast: () => ({ success: toastSuccess, error: vi.fn() }),
}))

vi.mock('@/store/auth', () => ({
  useAuth: () => ({ authData: { access: 'fake-access' } }),
}))

vi.mock('@/plugins/interceptor', () => ({
  default: httpClientMock,
}))

const { useUser } = await import('@/store/user')

describe('User Store', () => {
  let userStore

  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    userStore = useUser()
  })

  it('fetches a user profile successfully', async () => {
    const responseData = { username: 'test-user' }
    httpClientMock.get.mockResolvedValue({ status: 200, data: responseData })

    await userStore.getUserAction('test-user')

    expect(httpClientMock.get).toHaveBeenCalledWith('user/test-user', {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(userStore.user).toEqual(responseData)
    expect(userStore.loading).toBe(false)
  })

  it('fetches users list successfully with search query', async () => {
    const responseData = [{ username: 'test-user' }]
    httpClientMock.get.mockResolvedValue({ status: 200, data: responseData })

    await userStore.getUsersAction('search', 2)

    expect(httpClientMock.get).toHaveBeenCalledWith('user-search?search=search&page=2', {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(userStore.userData).toEqual(responseData)
    expect(userStore.loading).toBe(false)
  })

  it('follows a user successfully', async () => {
    httpClientMock.post.mockResolvedValue({ status: 200 })

    await userStore.followUserAction('target-user')

    expect(httpClientMock.post).toHaveBeenCalledWith('follow/target-user/', {}, {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(toastSuccess).toHaveBeenCalledWith('User followed!')
    expect(userStore.loading).toBe(false)
  })

  it('unfollows a user successfully', async () => {
    httpClientMock.delete.mockResolvedValue({ status: 204 })

    await userStore.unfollowUserAction('target-user')

    expect(httpClientMock.delete).toHaveBeenCalledWith('follow/target-user/', {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(toastSuccess).toHaveBeenCalledWith('User unfollowed!')
    expect(userStore.loading).toBe(false)
  })
})