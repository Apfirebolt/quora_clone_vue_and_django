import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

const httpClientMock = {
  get: vi.fn(),
}

vi.mock('@/store/auth', () => ({
  useAuth: () => ({ authData: { access: 'fake-access' } }),
}))

vi.mock('@/plugins/interceptor', () => ({
  default: httpClientMock,
}))

const { useNotification } = await import('@/store/notification')

describe('Notification Store', () => {
  let notificationStore

  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    notificationStore = useNotification()
  })

  it('fetches notifications successfully', async () => {
    const responseData = { results: ['notification-1'] }
    httpClientMock.get.mockResolvedValue({ status: 200, data: responseData })

    await notificationStore.getNotificationsAction(2)

    expect(httpClientMock.get).toHaveBeenCalledWith('notifications?page=2', {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(notificationStore.notifications).toEqual(responseData)
    expect(notificationStore.loading).toBe(false)
  })

  it('returns error when notification fetch fails', async () => {
    const error = new Error('Network problem')
    httpClientMock.get.mockRejectedValue(error)

    let result
    try {
      result = await notificationStore.getNotificationsAction(1)
    } catch (catchError) {
      result = catchError
    }

    expect(result).toBe(error)
    expect(notificationStore.loading).toBe(false)
  })

  it('resets notifications state', () => {
    notificationStore.notifications = { hello: 'world' }
    notificationStore.resetTagData()

    expect(notificationStore.notifications).toEqual({})
  })
})