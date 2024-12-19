<template>
    <header-component />
    <section class="bg-white shadow sm:rounded-lg" id="about">
      <div class="px-4 py-5 sm:p-6">
        <h2 class="text-3xl my-5 text-center text-red-800">MY ANSWERS</h2>
        <div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            List of answers and their questions
          </h3>
        </div>
  
        <div class="mt-5">
          <ul class="divide-y divide-gray-200">
            <li v-for="answer in answers" :key="answer.id" class="py-4">
              <div class="flex space-x-3">
                <div class="flex-1 space-y-1">
                  <p class="text-lg font-medium text-gray-900 my-1">
                    {{ answer.question_slug }}
                  </p>
                  <p class="text-sm font-medium text-gray-900">
                    {{ answer.body }}
                  </p>
                  <span class="text-sm font-medium text-gray-900"
                  >{{ answer.created_at }}</span>
                </div>
                <div>
                  <button
                    @click="updateAnswer(answer)"
                    class="text-blue-600 hover:text-blue-900 mx-2 px-2 py-1 rounded-md shadow-lg"
                  >
                    Edit
                  </button>
                  <button
                    @click="deleteAnswer(answer)"
                    class="text-red-600 hover:text-red-900 mx-2 px-2 py-1 rounded-md shadow-lg"
                  >
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
                    @confirmAction="deleteAnswerUtil"
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
  import AnswerForm from "../components/AnswerForm.vue";
  import ConfirmModal from "../components/Confirm.vue";
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
  const authStore = useAuth();
  const selectedAnswer = ref(null);
  const confirmMessage = ref("");
  const router = useRouter();
  
  const answers = computed(() => answerStore.getAnswers);
  
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
  
  const updateAnswerUtil = async (content) => {
    // copy all the properties of the answer object and replace the content and description
    const answer = { ...selectedAnswer.value, content };
  
    await answerStore.updateAnswer(answer);
    await answerStore.getMyAnswersAction();
    closeModal();
  };
  
  onMounted(async () => {
    await answerStore.getMyAnswersAction();
  });
  </script>
  