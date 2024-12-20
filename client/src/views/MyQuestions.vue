<template>
  <header-component />
  <section class="bg-white shadow sm:rounded-lg" id="about">
    <div class="px-4 py-5 sm:p-6">
      <h2 class="text-3xl my-5 text-center text-red-800">MY QUESTIONS</h2>
      <div>
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          List of questions you have asked and their answers
        </h3>
        <button
          @click="openModal"
          class="mt-3 inline-flex justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Add Question
        </button>
      </div>

      <div class="mt-5">
        <ul class="divide-y divide-gray-200">
          <li v-for="question in questions" :key="question.id" class="py-4">
            <div class="flex space-x-3">
              <div class="flex-1 space-y-1">
                <p class="text-sm font-medium text-gray-900">
                  {{ question.content }}
                </p>
                <p class="text-sm text-gray-500">
                  {{ question.description }}
                </p>
              </div>
              <div>
                <button
                  @click="updateQuestion(question)"
                  class="text-blue-600 hover:text-blue-900 mx-2 px-2 py-1 rounded-md shadow-lg"
                >
                  <PencilIcon class="h-5 w-5" />
                </button>
                <button
                  @click="viewQuestion(question)"
                  class="text-green-600 hover:text-green-900 mx-2 px-2 py-1 rounded-md shadow-lg"
                >
                  <EyeIcon class="h-5 w-5" />
                </button>
                <button
                  @click="deleteQuestion(question)"
                  class="text-red-600 hover:text-red-900 mx-2 px-2 py-1 rounded-md shadow-lg"
                >
                  <TrashIcon class="h-5 w-5" />
                </button>
              </div>
            </div>
          </li>
        </ul>
        <p v-if="questions.length === 0" class="text-center text-lg text-red-800">
          No questions found
        </p>
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
  </section>
  <footer-component />
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import QuestionForm from "../components/QuestionForm.vue";
import ConfirmModal from "../components/Confirm.vue";
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
const router = useRouter();

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
