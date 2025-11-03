<template>
  <header-component />
  <main class="bg-white shadow sm:rounded-lg" id="about">
    <div class="px-4 py-5 sm:p-6 container mx-auto">
      <section-header
        title="Dashboard"
        subtitle="Get the latest questions from people and topics you follow. Stay informed and engaged through sharing your opinions."
      />
      <div>
        <div
          v-if="
            notifications &&
            notifications.results &&
            notifications.results.length > 0
          "
          class="mb-4"
        >
          <button
            @click="toggleNotifications"
            class="flex items-center justify-between w-full p-3 bg-blue-50 rounded-lg border border-blue-200 hover:bg-blue-100 transition-colors"
          >
            <span class="font-medium text-blue-800">
              Notifications ({{ notifications.results.length }})
            </span>
            <svg
              :class="{ 'transform rotate-180': isNotificationsOpen }"
              class="w-5 h-5 text-blue-600 transition-transform"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </button>

          <transition
            enter-active-class="transition-all duration-300 ease-out"
            enter-from-class="opacity-0 max-h-0"
            enter-to-class="opacity-100 max-h-96"
            leave-active-class="transition-all duration-300 ease-out"
            leave-from-class="opacity-100 max-h-96"
            leave-to-class="opacity-0 max-h-0"
          >
            <div v-show="isNotificationsOpen" class="overflow-hidden">
              <div class="mt-2 p-3 bg-gray-50 rounded-lg border">
                <ul class="space-y-2">
                  <li
                    v-for="notification in notifications.results"
                    :key="notification.id"
                    class="py-3 px-2 bg-white rounded border-l-4 border-primary shadow-sm"
                  >
                    <div class="text-primary">
                      {{ notification.message || notification.content }}
                    </div>
                    <div class="text-xs text-gray-500 mt-1">
                      {{ notification.created_at || notification.timestamp }}
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </transition>
        </div>
        <div class="flex items-center space-x-4 mt-3">
          <button
            @click="openModal"
            class="inline-flex justify-center rounded-md border border-transparent bg-primary px-4 py-2 text-sm font-medium text-accent shadow-sm hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Add Question
          </button>
          <input
            v-model="searchText"
            @input="searchQuestions"
            type="text"
            placeholder="Search questions..."
            class="block w-4/5 rounded-md border-primary shadow-sm focus:border-accent px-2 py-3 focus:ring-primary sm:text-sm"
          />
        </div>
      </div>
      <div v-if="questions && questions.results" class="mt-5">
        <ul class="divide-y divide-gray-200">
          <li
            v-for="question in questions.results"
            :key="question.id"
            class="py-4"
          >
            <question-card
              :question="question"
              :deleteQuestion="deleteQuestion"
              :updateQuestion="updateQuestion"
              :viewQuestion="viewQuestion"
              :isQuestionOwner="isQuestionOwner"
            />
          </li>
        </ul>
      </div>
    </div>
    <TransitionRoot appear :show="isOpen" as="template">
      <Dialog as="div" @close="closeModal" class="relative z-10">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div
            class="flex min-h-full items-center justify-center p-4 text-center"
          >
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel
                class="w-full max-w-xl transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
              >
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

    <TransitionRoot appear :show="isConfirmModalOpen" as="template">
      <Dialog as="div" @close="closeConfirmModal" class="relative z-10">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div
            class="flex min-h-full items-center justify-center p-4 text-center"
          >
            <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel
                class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
              >
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
    if (value.length > 3) {
      searchQuestionUtil();
    } else {
      questionStore.getQuestionsAction();
    }
  }, 1000); // Adjust delay as needed (in milliseconds)
};

watch(searchText, debouncedSearch);

const searchQuestionUtil = () => {
  questionStore.getQuestionsAction(searchText.value);
};

const questions = computed(() => questionStore.getQuestions);
const notifications = computed(() => notificationStore.getNotifications);

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

const toggleNotifications = () => {
  isNotificationsOpen.value = !isNotificationsOpen.value;
};

const addQuestion = async (content, description) => {
  await questionStore.addQuestion(content, description);
  await questionStore.getQuestionsAction();
};

const deleteQuestion = async (question) => {
  selectedQuestion.value = question;
  confirmMessage.value = `Are you sure you want to delete the question: ${question.content}?`;
  openConfirmModal();
};

const deleteQuestionUtil = async () => {
  await questionStore.deleteQuestion(selectedQuestion.value.slug);
  await questionStore.getQuestionsAction();
  closeConfirmModal();
};

const updateQuestion = (question) => {
  selectedQuestion.value = question;
  openModal();
};

const updateQuestionUtil = async (content, description) => {
  // copy all the properties of the question object and replace the content and description
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
