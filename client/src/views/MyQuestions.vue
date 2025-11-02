<template>
  <header-component />
  <main class="bg-white shadow sm:rounded-lg" id="about">
    <section class="px-4 py-5 sm:p-6 container mx-auto">
      <SectionHeader title="My Questions" subtitle="Overview of your questions and their answers" />
      <div>
        <div class="flex items-center space-x-4 mt-3">
          <button
            @click="openModal"
            class="inline-flex justify-center rounded-md border border-transparent bg-primary px-4 py-2 text-sm font-medium text-accent shadow-sm hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Add Question
          </button>
          <input
            v-model="searchQuery"
            @input="searchQuestions"
            type="text"
            placeholder="Search questions..."
            class="block w-4/5 rounded-md border-primary shadow-sm focus:border-accent px-2 py-3 focus:ring-primary sm:text-sm"
          />
        </div>
      </div>

      <Loader v-if="isLoading" />

      <div v-if="questions && questions.results" class="mt-5">
        <ul class="divide-y divide-gray-200">
          <li v-for="question in filteredQuestions" :key="question.id" class="py-6 border-l-4 border-blue-500 pl-4 bg-gradient-to-r from-blue-50 to-white rounded-lg mb-4 shadow-md hover:shadow-lg transition-shadow duration-200">
            <div class="flex justify-between items-start">
              <div class="flex-1 space-y-3">
                <h3 class="text-lg font-semibold text-gray-800 leading-tight">
                  {{ question.content }}
                </h3>
                <p class="text-sm text-gray-600 leading-relaxed">
                  {{ question.description }}
                </p>
              </div>
              <div class="flex space-x-2 ml-4">
                <button
                  @click="updateQuestion(question)"
                  class="bg-blue-100 text-blue-700 hover:bg-blue-200 hover:text-blue-800 p-2 rounded-full transition-colors duration-200 shadow-sm"
                  title="Edit Question"
                >
                  <PencilIcon class="h-4 w-4" />
                </button>
                <button
                  @click="viewQuestion(question)"
                  class="bg-green-100 text-green-700 hover:bg-green-200 hover:text-green-800 p-2 rounded-full transition-colors duration-200 shadow-sm"
                  title="View Question"
                >
                  <EyeIcon class="h-4 w-4" />
                </button>
                <button
                  @click="deleteQuestion(question)"
                  class="bg-red-100 text-red-700 hover:bg-red-200 hover:text-red-800 p-2 rounded-full transition-colors duration-200 shadow-sm"
                  title="Delete Question"
                >
                  <TrashIcon class="h-4 w-4" />
                </button>
              </div>
            </div>
          </li>
        </ul>
        <p v-if="questions.length === 0" class="text-center text-lg text-red-800">
          No questions found
        </p>
      </div>
    </section>
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
}

function closeConfirmModal() {
  isConfirmModalOpen.value = false;
}

function openConfirmModal() {
  isConfirmModalOpen.value = true;
}

const filteredQuestions = computed(() => {
  return questions.value && questions.value.results.filter((question) => {
    return question.content.toLowerCase().includes(searchQuery.value.toLowerCase());
  });
});

const addQuestion = async (content, description) => {
  await questionStore.addQuestion(content, description);
  await questionStore.getMyQuestionsAction();
};

const deleteQuestion = async (question) => {
  selectedQuestion.value = question;
  confirmMessage.value = `Are you sure you want to delete the question: ${question.content}?`;
  openConfirmModal();
};

const deleteQuestionUtil = async () => {
  await questionStore.deleteQuestion(selectedQuestion.value.slug);
  await questionStore.getMyQuestionsAction();
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
