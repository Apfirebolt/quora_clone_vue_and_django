<template>
  <header-component />
  <main class="bg-white shadow sm:rounded-lg" id="about">
    <div class="px-4 py-5 sm:p-6 container mx-auto">
      <section-header
        title="Dashboard"
        subtitle="Get the latest questions from people and topics you follow. Stay informed and engaged through sharing your opinions."
      />
      <div>
        
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
            <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-gray-200 hover:shadow-lg transition-all duration-300 hover:border-indigo-300">
              <div class="flex justify-between items-start">
                <div class="flex-1 space-y-3">
                  <h3 class="text-lg font-semibold text-gray-900 leading-tight hover:text-indigo-600 transition-colors cursor-pointer">
                    {{ question.content }}
                  </h3>
                  <p class="text-gray-600 leading-relaxed">
                    {{ question.description }}
                  </p>
                  <div class="flex items-center space-x-4 text-sm text-gray-500">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                      By {{ question.author }}
                    </span>
                    <span>{{ new Date(question.created_at).toLocaleDateString() }}</span>
                  </div>
                </div>
                <div class="flex items-center space-x-2 ml-4">
                  <button
                    v-if="isQuestionOwner(question)"
                    @click="updateQuestion(question)"
                    class="inline-flex items-center justify-center w-10 h-10 text-blue-600 bg-blue-100 hover:bg-blue-200 rounded-full transition-all duration-200 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                    title="Edit question"
                  >
                    <PencilIcon class="h-5 w-5" />
                  </button>
                  <button
                    @click="viewQuestion(question)"
                    class="inline-flex items-center justify-center w-10 h-10 text-green-600 bg-green-100 hover:bg-green-200 rounded-full transition-all duration-200 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                    title="View question"
                  >
                    <EyeIcon class="h-5 w-5" />
                  </button>
                  <button
                    v-if="isQuestionOwner(question)"
                    @click="deleteQuestion(question)"
                    class="inline-flex items-center justify-center w-10 h-10 text-red-600 bg-red-100 hover:bg-red-200 rounded-full transition-all duration-200 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
                    title="Delete question"
                  >
                    <TrashIcon class="h-5 w-5" />
                  </button>
                </div>
              </div>
            </div>
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
                class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
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
import SectionHeader from "../components/SectionHeader.vue";
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
const confirmMessage = ref("");
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
});
</script>
