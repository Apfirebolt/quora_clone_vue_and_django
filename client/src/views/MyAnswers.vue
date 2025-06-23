<template>
  <header-component />
  <main class="bg-white shadow sm:rounded-lg" id="about">
    <div class="px-4 py-5 sm:p-6 container mx-auto">
      <h2 class="text-3xl my-5 text-center text-primary bg-accent py-2">MY ANSWERS</h2>
      <div>
        <Loader v-if="isLoading" />
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          List of answers and their questions
        </h3>
        <div class="flex items-center space-x-4 mt-3">
          <button @click="openModal"
            class="inline-flex justify-center rounded-md border border-transparent bg-primary px-4 py-2 text-sm font-medium text-accent shadow-sm hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Add Question
          </button>
          <input v-model="searchQuery" @input="searchQuestions" type="text" placeholder="Search answers..."
            class="block w-4/5 rounded-md border-primary shadow-sm focus:border-accent px-2 py-3 focus:ring-primary sm:text-sm" />
        </div>
      </div>

      <div v-if="answers && answers.results" class="mt-5">
        <ul class="divide-y divide-gray-200">
          <li v-for="answer in filteredAnswers" :key="answer.id" class="py-4">
            <div class="flex space-x-3">
              <div class="flex-1 space-y-1">
                <p class="text-lg font-medium text-gray-900 my-1">
                  <router-link :to="`/questions/${answer.question_slug}`" class="text-blue-600 hover:text-blue-800 hover:underline cursor-pointer">
                    {{ answer.question_slug }}
                  </router-link>
                </p>
                <p class="text-sm font-medium text-gray-900">
                  {{ answer.body }}
                </p>
                <span class="text-sm font-medium text-gray-900">{{ answer.created_at }}</span>
              </div>
              <div>
                <button @click="updateAnswer(answer)"
                  class="text-blue-600 hover:text-blue-900 mx-2 px-2 py-1 rounded-md shadow-lg">
                  Edit
                </button>
                <button @click="deleteAnswer(answer)"
                  class="text-red-600 hover:text-red-900 mx-2 px-2 py-1 rounded-md shadow-lg">
                  Delete
                </button>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <TransitionRoot appear :show="isOpen" as="template">
      <Dialog as="div" @close="closeModal" class="relative z-10">
        <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0" enter-to="opacity-100"
          leave="duration-200 ease-in" leave-from="opacity-100" leave-to="opacity-0">
          <div class="fixed inset-0 bg-black/25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100" leave="duration-200 ease-in" leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95">
              <DialogPanel
                class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <answer-form :closeModal="closeModal" :answer="selectedAnswer" :updateAnswer="updateAnswerUtil" />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <TransitionRoot appear :show="isConfirmModalOpen" as="template">
      <Dialog as="div" @close="closeConfirmModal" class="relative z-10">
        <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0" enter-to="opacity-100"
          leave="duration-200 ease-in" leave-from="opacity-100" leave-to="opacity-0">
          <div class="fixed inset-0 bg-black/25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100" leave="duration-200 ease-in" leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95">
              <DialogPanel
                class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <confirm-modal :message="confirmMessage" @confirmAction="deleteAnswerUtil"
                  @cancelAction="closeConfirmModal" />
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
import AnswerForm from "../components/AnswerForm.vue";
import ConfirmModal from "../components/Confirm.vue";
import Loader from "../components/Loader.vue";
import { useAnswer } from "../store/answer";
import { useAuth } from "../store/auth";
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

const filteredAnswers = computed(() => {
  return answers.value && answers.value.results.filter((answer) => {
    const query = searchQuery.value.toLowerCase();
    return (
      answer.body.toLowerCase().includes(query) ||
      answer.question_slug.toLowerCase().includes(query)
    );
  });
});

const deleteAnswer = async (answer) => {
  selectedAnswer.value = answer;
  confirmMessage.value = `Are you sure you want to delete the answer: ${answer.body}?`;
  openConfirmModal();
};

const deleteAnswerUtil = async () => {
  await answerStore.deleteAnswer(selectedAnswer.value.uuid);
  await answerStore.getMyAnswersAction();
  closeConfirmModal();
};

const updateAnswer = (answer) => {
  selectedAnswer.value = answer;
  openModal();
};

const updateAnswerUtil = async (body) => {
  // copy all the properties of the answer object and replace the content and description
  const answer = { ...selectedAnswer.value, body };

  await answerStore.updateAnswer(answer);
  await answerStore.getMyAnswersAction();
  closeModal();
};

onMounted(async () => {
  await answerStore.getMyAnswersAction();
});
</script>