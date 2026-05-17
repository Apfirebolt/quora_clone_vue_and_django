import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

const toastSuccess = vi.fn()
const httpClientMock = {
  get: vi.fn(),
  post: vi.fn(),
  put: vi.fn(),
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

const { useTag } = await import('@/store/tag')

describe('Tag Store', () => {
  let tagStore

  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    tagStore = useTag()
  })

  it('adds a tag successfully', async () => {
    const payload = { name: 'javascript' }
    httpClientMock.post.mockResolvedValue({ status: 201 })

    await tagStore.addTag('question-slug', payload)

    expect(httpClientMock.post).toHaveBeenCalledWith('tags/', payload, {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(toastSuccess).toHaveBeenCalledWith('Tag added!')
    expect(tagStore.loading).toBe(false)
  })

  it('updates a tag successfully', async () => {
    const payload = { uuid: 'tag-123', name: 'vue' }
    httpClientMock.put.mockResolvedValue({ status: 200 })

    await tagStore.updateTag(payload)

    expect(httpClientMock.put).toHaveBeenCalledWith('tags/tag-123/', payload, {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(toastSuccess).toHaveBeenCalledWith('Tag updated!')
    expect(tagStore.loading).toBe(false)
  })

  it('fetches tags successfully', async () => {
    const responseData = [{ uuid: 'tag-1' }]
    httpClientMock.get.mockResolvedValue({ status: 200, data: responseData })

    await tagStore.getTagsAction(3)

    expect(httpClientMock.get).toHaveBeenCalledWith('tags?page=3', {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(tagStore.tagData).toEqual(responseData)
    expect(tagStore.loading).toBe(false)
  })

  it('deletes a tag successfully', async () => {
    httpClientMock.delete.mockResolvedValue({ status: 204 })

    await tagStore.deleteTag('tag-123')

    expect(httpClientMock.delete).toHaveBeenCalledWith('tags/tag-123', {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(toastSuccess).toHaveBeenCalledWith('Tag deleted!')
  })
})