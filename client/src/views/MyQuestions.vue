<template>
  <header-component />

  <main class="min-h-[calc(100vh-4rem)] bg-neutral/10 py-10 px-4 sm:px-6 lg:px-8" id="about">
    <div class="mx-auto max-w-6xl space-y-8">
      
      <!-- Top Section Header & Actions Bar -->
      <div class="rounded-3xl border border-gray-100 bg-white p-6 sm:p-8 shadow-sm">
        <div class="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
          <SectionHeader
            title="My Questions"
            subtitle="Overview of your questions and their answers"
          />

          <!-- Action Controls -->
          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full sm:w-auto">
            <!-- Search Bar -->
            <div class="relative w-full sm:w-80">
              <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-gray-400">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </span>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search questions..."
                class="w-full rounded-xl border border-gray-200 bg-gray-50/60 py-2.5 pl-10 pr-4 text-sm text-gray-900 placeholder-gray-400 transition focus:border-primary focus:bg-white focus:outline-none focus:ring-2 focus:ring-primary/20"
              />
            </div>

            <!-- Add Question Button -->
            <button
              @click="openModal"
              type="button"
              class="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-accent shadow-sm transition hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-primary/40 active:scale-[0.98]"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
              </svg>
              <span>Add Question</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <Loader v-if="isLoading" />

      <!-- Questions List -->
      <div v-else-if="filteredQuestions && filteredQuestions.length > 0" class="space-y-4">
        <article
          v-for="question in filteredQuestions"
          :key="question.id"
          class="group relative rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-md"
        >
          <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
            <!-- Question Content -->
            <div class="flex-1 space-y-2.5 min-w-0">
              <div class="flex items-center gap-2">
                <span class="inline-flex items-center rounded-md bg-blue-50 px-2 py-0.5 text-xs font-semibold text-blue-700 ring-1 ring-inset ring-blue-700/10">
                  Question
                </span>
                <span v-if="question.created_at" class="text-xs text-slate-400">
                  {{ formatDate(question.created_at) }}
                </span>
              </div>

              <h3
                @click="viewQuestion(question)"
                class="cursor-pointer text-lg font-semibold tracking-tight text-slate-900 transition-colors hover:text-primary leading-snug line-clamp-2"
              >
                {{ question.content }}
              </h3>

              <p class="text-sm text-slate-600 leading-relaxed line-clamp-3">
                {{ question.description }}
              </p>
            </div>

            <!-- Segmented Action Toolbar -->
            <div class="flex items-center gap-1 self-end sm:self-start rounded-xl bg-slate-50 p-1 border border-slate-100 shrink-0">
              <button
                @click="viewQuestion(question)"
                class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 transition hover:bg-white hover:text-indigo-600 hover:shadow-xs focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                title="View Question"
              >
                <EyeIcon class="h-4 w-4" />
              </button>
              <button
                @click="updateQuestion(question)"
                class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 transition hover:bg-white hover:text-blue-600 hover:shadow-xs focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                title="Edit Question"
              >
                <PencilIcon class="h-4 w-4" />
              </button>
              <button
                @click="deleteQuestion(question)"
                class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 transition hover:bg-white hover:text-rose-600 hover:shadow-xs focus:outline-none focus:ring-2 focus:ring-rose-500/20"
                title="Delete Question"
              >
                <TrashIcon class="h-4 w-4" />
              </button>
            </div>
          </div>
        </article>
      </div>

      <!-- Empty State -->
      <div
        v-else
        class="rounded-3xl border border-dashed border-slate-200 bg-white p-12 text-center"
      >
        <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-slate-100 text-slate-400">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="mt-4 text-sm font-semibold text-slate-900">No questions found</h3>
        <p class="mt-1 text-sm text-slate-500">
          {{ searchQuery ? `No results match "${searchQuery}".` : "You haven't posted any questions yet." }}
        </p>
      </div>

    </div>

    <!-- Question Modal -->
    <TransitionRoot appear :show="isOpen" as="template">
      <Dialog as="div" @close="closeModal" class="relative z-50">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-neutral-950/60 backdrop-blur-xs" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-xl transform overflow-hidden rounded-3xl bg-white p-6 sm:p-8 text-left align-middle shadow-2xl border border-slate-100 transition-all">
                <question-form
                  :closeModal="closeModal"
                  :addQuestion="addQuestion"
                  :question="selectedQuestion"
                  :updateQuestion="updateQuestionUtil"
                />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Confirmation Modal -->
    <TransitionRoot appear :show="isConfirmModalOpen" as="template">
      <Dialog as="div" @close="closeConfirmModal" class="relative z-50">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-neutral-950/60 backdrop-blur-xs" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-3xl bg-white p-6 sm:p-8 text-left align-middle shadow-2xl border border-slate-100 transition-all">
                <confirm-modal
                  :message="confirmMessage"
                  @confirmAction="deleteQuestionUtil"
                  @cancelAction="closeConfirmModal"
                />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </main>

  <footer-component />
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import QuestionForm from "../components/QuestionForm.vue";
import ConfirmModal from "../components/Confirm.vue";
import SectionHeader from "../components/SectionHeader.vue";
import Loader from "../components/Loader.vue";
import { useQuestion } from "../store/question";
import { useAuth } from "../store/auth";
import { PencilIcon, TrashIcon, EyeIcon } from "@heroicons/vue/outline";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
} from "@headlessui/vue";

const isOpen = ref(false);
const isConfirmModalOpen = ref(false);
const questionStore = useQuestion();
const authStore = useAuth();
const selectedQuestion = ref(null);
const searchQuery = ref("");
const confirmMessage = ref("");
const router = useRouter();

const questions = computed(() => questionStore.getQuestions);
const isLoading = computed(() => questionStore.isLoading);

function closeModal() {
  isOpen.value = false;
}

function openModal() {
  isOpen.value = true;
  selectedQuestion.value = null;
}

function closeConfirmModal() {
  isConfirmModalOpen.value = false;
}

function openConfirmModal() {
  isConfirmModalOpen.value = true;
}

const formatDate = (dateString) => {
  if (!dateString) return "";
  return new Date(dateString).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

const filteredQuestions = computed(() => {
  if (!questions.value || !questions.value.results) return [];
  const query = searchQuery.value.toLowerCase().trim();
  if (!query) return questions.value.results;

  return questions.value.results.filter((question) => {
    return (
      question.content?.toLowerCase().includes(query) ||
      question.description?.toLowerCase().includes(query)
    );
  });
});

const addQuestion = async (content, description) => {
  const data = {
    content: content,
    description: description,
  };
  await questionStore.addQuestion(data);
  await questionStore.getMyQuestionsAction();
};

const deleteQuestion = async (question) => {
  selectedQuestion.value = question;
  confirmMessage.value = `Are you sure you want to delete the question: "${question.content}"?`;
  openConfirmModal();
};

const deleteQuestionUtil = async () => {
  await questionStore.deleteQuestion(selectedQuestion.value.slug);
  await questionStore.getMyQuestionsAction();
  closeConfirmModal();
};

const updateQuestion = (question) => {
  selectedQuestion.value = question;
  isOpen.value = true;
};

const updateQuestionUtil = async (content, description) => {
  const question = { ...selectedQuestion.value, content, description };
  await questionStore.updateQuestion(question);
  await questionStore.getMyQuestionsAction();
  closeModal();
};

const viewQuestion = async (question) => {
  router.push({ name: "QuestionDetail", params: { slug: question.slug } });
};

onMounted(() => {
  questionStore.getMyQuestionsAction();
});
</script>