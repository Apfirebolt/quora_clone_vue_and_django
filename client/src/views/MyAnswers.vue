<template>
  <header-component />
  <main class="bg-white shadow sm:rounded-lg" id="about">
    <div class="px-4 py-5 sm:p-6 container mx-auto">
      <SectionHeader title="My Answers" subtitle="Overview of your answers and their questions" />
      <div>
        <Loader v-if="isLoading" />
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
        <div class="grid gap-6 md:grid-cols-2">
          <div v-for="answer in filteredAnswers" :key="answer.id" 
           class="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 p-6">
        <div class="flex flex-col h-full">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900 mb-3">
          <router-link :to="`/questions/${answer.question_slug}`" 
               class="text-blue-600 hover:text-blue-800 hover:underline cursor-pointer">
            {{ answer.question_slug }}
          </router-link>
            </h3>
            <p class="text-gray-700 text-sm mb-4 line-clamp-3">
          {{ answer.body }}
            </p>
            <span class="text-xs text-gray-500">{{ answer.created_at }}</span>
          </div>
            <div class="flex justify-end space-x-2 mt-4 pt-4 border-t border-gray-200">
            <button @click="updateAnswer(answer)"
              class="inline-flex items-center px-3 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition duration-200">
              <PencilIcon class="h-5 w-5 mr-1" />
            </button>
            <button @click="deleteAnswer(answer)"
              class="inline-flex items-center px-3 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition duration-200">
              <TrashIcon class="h-5 w-5 mr-1" />
            </button>
            </div>
        </div>
          </div>
        </div>
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
import SectionHeader from "../components/SectionHeader.vue";
import { useAnswer } from "../store/answer";
import { useAuth } from "../store/auth";
// import icons here
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