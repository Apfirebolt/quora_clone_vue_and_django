import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

const toastSuccess = vi.fn()
const toastError = vi.fn()
const httpClientMock = {
  get: vi.fn(),
  post: vi.fn(),
  put: vi.fn(),
  delete: vi.fn(),
}

vi.mock('vue-toastification', () => ({
  useToast: () => ({ success: toastSuccess, error: toastError }),
}))

vi.mock('@/store/auth', () => ({
  useAuth: () => ({ authData: { access: 'fake-access' } }),
}))

vi.mock('@/plugins/interceptor', () => ({
  default: httpClientMock,
}))

const { useAnswer } = await import('@/store/answer')

describe('Answer Store', () => {
  let answerStore

  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    answerStore = useAnswer()
  })

  it('adds an answer successfully', async () => {
    const payload = { body: 'Test answer' }
    httpClientMock.post.mockResolvedValue({ status: 201 })

    await answerStore.addAnswer('question-slug', payload)

    expect(httpClientMock.post).toHaveBeenCalledWith('questions-new-answer/question-slug/', payload, {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(toastSuccess).toHaveBeenCalledWith('Answer added!')
    expect(answerStore.loading).toBe(false)
  })

  it('returns error when adding an answer fails', async () => {
    const error = new Error('Add answer failed')
    httpClientMock.post.mockRejectedValue(error)

    let result
    try {
      result = await answerStore.addAnswer('question-slug', { body: 'Test' })
    } catch (catchError) {
      result = catchError
    }

    expect(result).toBe(error)
    expect(answerStore.loading).toBe(false)
  })

  it('updates answer successfully', async () => {
    const answerData = { uuid: 'abc-123', body: 'Updated answer' }
    httpClientMock.put.mockResolvedValue({ status: 200 })

    await answerStore.updateAnswer(answerData)

    expect(httpClientMock.put).toHaveBeenCalledWith('answers/abc-123/', answerData, {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(toastSuccess).toHaveBeenCalledWith('Answer updated!')
    expect(answerStore.loading).toBe(false)
  })

  it('fetches answers and stores page data', async () => {
    const responseData = [{ uuid: '123' }]
    httpClientMock.get.mockResolvedValue({ status: 200, data: responseData })

    await answerStore.getAnswersAction(3)

    expect(httpClientMock.get).toHaveBeenCalledWith('answers?page=3', {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(answerStore.answerData).toEqual(responseData)
    expect(answerStore.loading).toBe(false)
  })

  it('deletes an answer successfully', async () => {
    httpClientMock.delete.mockResolvedValue({ status: 204 })

    await answerStore.deleteAnswer('answer-123')

    expect(httpClientMock.delete).toHaveBeenCalledWith('answers/answer-123', {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(toastSuccess).toHaveBeenCalledWith('Answer deleted!')
  })
})