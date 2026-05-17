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

const { useQuestion } = await import('@/store/question')

describe('Question Store', () => {
  let questionStore

  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    questionStore = useQuestion()
  })

  it('adds a question successfully', async () => {
    const payload = { title: 'Test question' }
    httpClientMock.post.mockResolvedValue({ status: 201 })

    await questionStore.addQuestion(payload)

    expect(httpClientMock.post).toHaveBeenCalledWith('questions', payload, {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(toastSuccess).toHaveBeenCalledWith('Question added!')
    expect(questionStore.loading).toBe(false)
  })

  it('returns error when adding a question fails', async () => {
    const error = new Error('Server error')
    httpClientMock.post.mockRejectedValue(error)

    let result
    try {
      result = await questionStore.addQuestion({})
    } catch (catchError) {
      result = catchError
    }

    expect(result).toBe(error)
    expect(questionStore.loading).toBe(false)
  })

  it('fetches a question by slug successfully', async () => {
    const slug = 'my-question'
    const responseData = { slug, content: 'Test' }
    httpClientMock.get.mockResolvedValue({ status: 200, data: responseData })

    await questionStore.getQuestionAction(slug)

    expect(httpClientMock.get).toHaveBeenCalledWith('questions/' + slug, {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(questionStore.question).toEqual(responseData)
  })

  it('fetches paginated questions successfully', async () => {
    const responseData = [{ slug: 'q1' }]
    httpClientMock.get.mockResolvedValue({ status: 200, data: responseData })

    await questionStore.getQuestionsAction('search-term', 2)

    expect(httpClientMock.get).toHaveBeenCalledWith('questions?page=2&search=search-term', {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(questionStore.questionData).toEqual(responseData)
  })

  it('deletes a question successfully', async () => {
    const slug = 'delete-me'
    httpClientMock.delete.mockResolvedValue({ status: 204 })

    await questionStore.deleteQuestion(slug)

    expect(httpClientMock.delete).toHaveBeenCalledWith('questions/' + slug, {
      headers: { Authorization: 'Bearer fake-access' },
    })
    expect(toastSuccess).toHaveBeenCalledWith('Question deleted!')
  })
})