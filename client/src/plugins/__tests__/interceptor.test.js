import { describe, it, expect, beforeEach, vi } from 'vitest'

const toastError = vi.fn()
const routerPush = vi.fn()
const logout = vi.fn()

vi.mock('vue-toastification', () => ({
  useToast: () => ({ error: toastError }),
}))

vi.mock('@/routes', () => ({
  default: { push: routerPush },
}))

vi.mock('@/store/auth', () => ({
  useAuth: () => ({ logout }),
}))

const { default: httpClient } = await import('@/plugins/interceptor')

const getResponseRejector = () => httpClient.interceptors.response.handlers[0].rejected

describe('HTTP interceptor', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('redirects to login and logs out on 401 response', () => {
    const rejected = getResponseRejector()
    const error = { response: { status: 401, data: { message: 'Unauthorized' } } }

    const ret = rejected(error)
    expect(ret).toBeUndefined()
    expect(toastError).toHaveBeenCalledWith('You are not authorized to access this resource')
    expect(routerPush).toHaveBeenCalledWith('/login')
    expect(logout).toHaveBeenCalled()
  })

  it('redirects to login and logs out on 403 response', () => {
    const rejected = getResponseRejector()
    const error = { response: { status: 403, data: { message: 'Forbidden' } } }

    const ret = rejected(error)
    expect(ret).toBeUndefined()
    expect(toastError).toHaveBeenCalledWith('You are not authorized to access this resource')
    expect(routerPush).toHaveBeenCalledWith('/login')
    expect(logout).toHaveBeenCalled()
  })

  it('redirects to not-found on 404 response', () => {
    const rejected = getResponseRejector()
    const error = { response: { status: 404, data: { message: 'Not found' } } }

    const ret = rejected(error)
    expect(ret).toBeUndefined()
    expect(toastError).toHaveBeenCalledWith('Resource not found')
    expect(routerPush).toHaveBeenCalledWith('/not-found')
  })

  it('redirects to server-error on 500 response', () => {
    const rejected = getResponseRejector()
    const error = { response: { status: 500, data: { message: 'Server error' } } }

    const ret = rejected(error)
    expect(ret).toBeUndefined()
    expect(toastError).toHaveBeenCalledWith('Internal server error')
    expect(routerPush).toHaveBeenCalledWith('/server-error')
  })

  it('rejects the promise on 400 response', async () => {
    const rejected = getResponseRejector()
    const error = { response: { status: 400, data: { message: 'Bad request' } } }

    await expect(rejected(error)).rejects.toBe(error)
    expect(toastError).not.toHaveBeenCalledWith('You are not authorized to access this resource')
  })

  it('rejects the promise and shows custom toast on unknown response', async () => {
    const rejected = getResponseRejector()
    const error = { response: { status: 422, data: { message: 'Validation failed' } } }

    await expect(rejected(error)).rejects.toBe(error)
    expect(toastError).toHaveBeenCalledWith('Validation failed')
  })
})
