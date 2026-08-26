<template>
  <header-component />

  <main class="min-h-[calc(100vh-4rem)] bg-neutral/10 py-10 px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-6xl space-y-8">
      
      <!-- Top Section Header & Actions Bar -->
      <div class="rounded-3xl border border-gray-100 bg-white p-6 sm:p-8 shadow-sm">
        <div class="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
          <SectionHeader
            title="My Answers"
            subtitle="Overview of your contributed answers and questions"
          />

          <!-- Action Controls -->
          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full sm:w-auto">
            <!-- Search Bar -->
            <div class="relative w-full sm:w-72">
              <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-gray-400">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </span>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search answers..."
                class="w-full rounded-xl border border-gray-200 bg-gray-50/60 py-2.5 pl-10 pr-4 text-sm text-gray-900 placeholder-gray-400 transition focus:border-primary focus:bg-white focus:outline-none focus:ring-2 focus:ring-primary/20"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Content Area -->
      <Loader v-if="isLoading" />

      <!-- Answers Grid -->
      <div v-else-if="filteredAnswers && filteredAnswers.length > 0" class="grid gap-5 md:grid-cols-2">
        <article
          v-for="answer in filteredAnswers"
          :key="answer.id || answer.uuid"
          class="group relative flex flex-col justify-between rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-md"
        >
          <div class="space-y-3">
            <!-- Question Reference Badge / Header -->
            <div class="flex items-start justify-between gap-3">
              <span class="inline-flex items-center rounded-md bg-blue-50 px-2.5 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10">
                Question
              </span>
              <span class="text-xs text-slate-400">
                {{ formatDate(answer.created_at) }}
              </span>
            </div>

            <!-- Question Link -->
            <h3 class="text-base font-semibold text-slate-900 group-hover:text-primary transition-colors">
              <router-link
                :to="`/questions/${answer.question_slug}`"
                class="hover:underline line-clamp-2 leading-snug"
              >
                {{ formatQuestionTitle(answer.question_slug) }}
              </router-link>
            </h3>

            <!-- Answer Body -->
            <p class="text-sm text-slate-600 leading-relaxed line-clamp-3">
              {{ answer.body }}
            </p>
          </div>

          <!-- Bottom Actions Toolbar -->
          <div class="mt-6 flex items-center justify-between border-t border-slate-100 pt-4">
            <router-link
              :to="`/questions/${answer.question_slug}`"
              class="inline-flex items-center gap-1 text-xs font-semibold text-primary transition hover:text-secondary"
            >
              <span>View context</span>
              <span class="transition-transform group-hover:translate-x-0.5">→</span>
            </router-link>

            <div class="flex items-center gap-1 rounded-xl bg-slate-50 p-1 border border-slate-100">
              <button
                @click="updateAnswer(answer)"
                class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 transition hover:bg-white hover:text-blue-600 hover:shadow-xs focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                title="Edit Answer"
              >
                <PencilIcon class="h-4 w-4" />
              </button>
              <button
                @click="deleteAnswer(answer)"
                class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 transition hover:bg-white hover:text-rose-600 hover:shadow-xs focus:outline-none focus:ring-2 focus:ring-rose-500/20"
                title="Delete Answer"
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
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <h3 class="mt-4 text-sm font-semibold text-slate-900">No answers found</h3>
        <p class="mt-1 text-sm text-slate-500">
          {{ searchQuery ? "No results match your search term." : "You haven't contributed any answers yet." }}
        </p>
      </div>

    </div>

    <!-- Edit Answer Modal -->
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
                <answer-form
                  :closeModal="closeModal"
                  :answer="selectedAnswer"
                  :updateAnswer="updateAnswerUtil"
                />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Confirm Deletion Modal -->
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
              <DialogPanel class="w-full max-w-lg transform overflow-hidden rounded-3xl bg-white p-6 sm:p-8 text-left align-middle shadow-2xl border border-slate-100 transition-all">
                <confirm-modal
                  :message="confirmMessage"
                  @confirmAction="deleteAnswerUtil"
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
import AnswerForm from "../components/AnswerForm.vue";
import ConfirmModal from "../components/Confirm.vue";
import Loader from "../components/Loader.vue";
import SectionHeader from "../components/SectionHeader.vue";
import { useAnswer } from "../store/answer";
import { PencilIcon, TrashIcon } from "@heroicons/vue/outline";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
} from "@headlessui/vue";

const isOpen = ref(false);
const isConfirmModalOpen = ref(false);
const answerStore = useAnswer();
const selectedAnswer = ref(null);
const confirmMessage = ref("");
const searchQuery = ref("");

const answers = computed(() => answerStore.getAnswers);
const isLoading = computed(() => answerStore.isLoading);

function closeModal() {
  isOpen.value = false;
}

function openModal() {
  isOpen.value = true;
}

function closeConfirmModal() {
  isConfirmModalOpen.value = false;
}

function openConfirmModal() {
  isConfirmModalOpen.value = true;
}

const formatQuestionTitle = (slug) => {
  if (!slug) return "";
  return slug.replace(/-/g, " ");
};

const formatDate = (dateString) => {
  if (!dateString) return "";
  return new Date(dateString).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

const filteredAnswers = computed(() => {
  if (!answers.value || !answers.value.results) return [];
  const query = searchQuery.value.toLowerCase().trim();
  if (!query) return answers.value.results;

  return answers.value.results.filter((answer) => {
    return (
      answer.body?.toLowerCase().includes(query) ||
      answer.question_slug?.toLowerCase().includes(query)
    );
  });
});

const deleteAnswer = (answer) => {
  selectedAnswer.value = answer;
  confirmMessage.value = `Are you sure you want to delete this answer?`;
  openConfirmModal();
};

const deleteAnswerUtil = async () => {
  await answerStore.deleteAnswer(selectedAnswer.value.uuid || selectedAnswer.value.id);
  await answerStore.getMyAnswersAction();
  closeConfirmModal();
};

const updateAnswer = (answer) => {
  selectedAnswer.value = answer;
  openModal();
};

const updateAnswerUtil = async (body) => {
  const answer = { ...selectedAnswer.value, body };
  await answerStore.updateAnswer(answer);
  await answerStore.getMyAnswersAction();
  closeModal();
};

onMounted(async () => {
  await answerStore.getMyAnswersAction();
});
</script>