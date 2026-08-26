<template>
  <header-component />

  <main class="min-h-[calc(100vh-4rem)] bg-neutral/10 py-10 px-4 sm:px-6 lg:px-8 font-inter" id="about">
    <div class="mx-auto max-w-5xl space-y-6">
      
      <!-- Top Header & Action Controls -->
      <div class="rounded-3xl border border-gray-100 bg-white p-6 sm:p-8 shadow-sm">
        <div class="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
          <section-header
            title="Dashboard"
            subtitle="Get the latest questions from people and topics you follow. Stay informed and engaged."
          />

          <!-- Actions Bar -->
          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full sm:w-auto">
            <!-- Search Bar -->
            <div class="relative w-full sm:w-72">
              <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-gray-400">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </span>
              <input
                v-model="searchText"
                type="text"
                placeholder="Search questions..."
                class="w-full rounded-xl border border-gray-200 bg-gray-50/60 py-2.5 pl-10 pr-4 text-sm text-gray-900 placeholder-gray-400 transition focus:border-primary focus:bg-white focus:outline-none focus:ring-2 focus:ring-primary/20"
              />
            </div>

            <!-- Add Question CTA -->
            <button
              @click="openModal"
              type="button"
              class="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-accent shadow-sm transition-all hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-primary/40 active:scale-[0.98]"
            >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
              </svg>
              <span>Add Question</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Collapsible Notification Center -->
      <div
        v-if="notifications && notifications.results && notifications.results.length > 0"
        class="overflow-hidden rounded-2xl border border-blue-100 bg-accent shadow-xs backdrop-blur-sm"
      >
        <button
          @click="toggleNotifications"
          type="button"
          class="flex w-full items-center justify-between px-5 py-3.5 text-left transition hover:bg-blue-100/50 focus:outline-none"
        >
          <div class="flex items-center gap-2.5">
            <span class="flex h-2 w-2 rounded-full bg-primary animate-pulse"></span>
            <span class="text-xs font-bold uppercase tracking-wider text-blue-900">
              Notifications
            </span>
            <span class="rounded-full bg-blue-200/80 px-2 py-0.5 text-[11px] font-semibold text-blue-800">
              {{ notifications.results.length }}
            </span>
          </div>

          <svg
            :class="{ 'rotate-180': isNotificationsOpen }"
            class="h-4 w-4 text-blue-700 transition-transform duration-200"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        <transition
          enter-active-class="transition-all duration-300 ease-out"
          enter-from-class="opacity-0 max-h-0"
          enter-to-class="opacity-100 max-h-96"
          leave-active-class="transition-all duration-200 ease-in"
          leave-from-class="opacity-100 max-h-96"
          leave-to-class="opacity-0 max-h-0"
        >
          <div v-show="isNotificationsOpen" class="border-t border-blue-100/80 bg-white/70 px-5 py-3 overflow-y-auto max-h-72">
            <ul class="space-y-2.5">
              <li
                v-for="notification in notifications.results"
                :key="notification.id"
                class="flex items-start justify-between gap-4 rounded-xl border border-slate-100 bg-white p-3.5 shadow-2xs transition hover:border-slate-200"
              >
                <div class="space-y-1 min-w-0">
                  <p class="text-xs sm:text-sm font-medium text-slate-800 leading-snug">
                    {{ notification.message || notification.content }}
                  </p>
                  <p class="text-[11px] text-slate-400">
                    {{ notification.created_at || notification.timestamp }}
                  </p>
                </div>
              </li>
            </ul>
          </div>
        </transition>
      </div>

      <!-- Feed / Questions List -->
      <div v-if="questions && questions.results && questions.results.length > 0" class="space-y-4">
        <div v-for="question in questions.results" :key="question.id">
          <question-card
            :question="question"
            :deleteQuestion="deleteQuestion"
            :updateQuestion="updateQuestion"
            :viewQuestion="viewQuestion"
            :isQuestionOwner="isQuestionOwner"
          />
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-else
        class="rounded-3xl border border-dashed border-slate-200 bg-white p-12 text-center"
      >
        <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-slate-100 text-slate-400">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <h3 class="mt-4 text-sm font-semibold text-slate-900">No questions found</h3>
        <p class="mt-1 text-sm text-slate-500">
          {{ searchText ? `No questions matching "${searchText}".` : "Be the first to start a conversation in the community." }}
        </p>
      </div>

    </div>

    <!-- Create/Edit Modal -->
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
import { ref, watch, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import QuestionForm from "../components/QuestionForm.vue";
import ConfirmModal from "../components/Confirm.vue";
import QuestionCard from "../components/QuestionCard.vue";
import SectionHeader from "../components/SectionHeader.vue";
import { useQuestion } from "../store/question";
import { useNotification } from "../store/notification";
import { useAuth } from "../store/auth";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
} from "@headlessui/vue";

const isOpen = ref(false);
const isConfirmModalOpen = ref(false);
const questionStore = useQuestion();
const notificationStore = useNotification();
const authStore = useAuth();
const selectedQuestion = ref(null);
const confirmMessage = ref("");
const isNotificationsOpen = ref(false);
const searchText = ref("");
const router = useRouter();
let timeoutId;

const debouncedSearch = (value) => {
  if (timeoutId) clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    if (value && value.trim().length > 3) {
      searchQuestionUtil();
    } else {
      questionStore.getQuestionsAction();
    }
  }, 400);
};

watch(searchText, debouncedSearch);

const searchQuestionUtil = () => {
  questionStore.getQuestionsAction(searchText.value.trim());
};

const questions = computed(() => questionStore.getQuestions);
const notifications = computed(() => notificationStore.getNotifications);

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

const toggleNotifications = () => {
  isNotificationsOpen.value = !isNotificationsOpen.value;
};

const addQuestion = async (content, description) => {
  const data = {
    content: content,
    description: description,
  };
  await questionStore.addQuestion(data);
  await questionStore.getQuestionsAction();
};

const deleteQuestion = async (question) => {
  selectedQuestion.value = question;
  confirmMessage.value = `Are you sure you want to delete "${question.content}"?`;
  openConfirmModal();
};

const deleteQuestionUtil = async () => {
  await questionStore.deleteQuestion(selectedQuestion.value.slug);
  await questionStore.getQuestionsAction();
  closeConfirmModal();
};

const updateQuestion = (question) => {
  selectedQuestion.value = question;
  isOpen.value = true;
};

const updateQuestionUtil = async (content, description) => {
  const question = { ...selectedQuestion.value, content, description };
  await questionStore.updateQuestion(question);
  await questionStore.getQuestionsAction();
  closeModal();
};

const viewQuestion = async (question) => {
  router.push({ name: "QuestionDetail", params: { slug: question.slug } });
};

const isQuestionOwner = computed(() => {
  return (question) =>
    authStore.authData && question.author === authStore.authData.email;
});

onMounted(() => {
  questionStore.getQuestionsAction();
  notificationStore.getNotificationsAction();
});
</script>