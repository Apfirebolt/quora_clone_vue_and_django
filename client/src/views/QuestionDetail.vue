<template>
  <header-component />
  <main class="bg-white shadow sm:rounded-lg" id="about">
    <section class="px-4 py-5 sm:p-6 container mx-auto">
      <h2 class="text-3xl my-5 text-center text-primary bg-accent py-2">{{ question.content }}</h2>
      <div class="flex justify-between">
        <Loader v-if="isQuestionLoading" />
        <div>
          <p class="my-3">Asked by: {{ question.author }}</p>
          <p v-if="showUsersUpvotedByText" class="my-2 bg-success text-white p-2 rounded-lg">
            {{ showUsersUpvotedByText }}
          </p>
          <p v-if="showUsersDownvotedByText" class="my-2 bg-danger text-white p-2 rounded-lg">
            {{ showUsersDownvotedByText }}
          </p>
          <div class="mt-2 max-w-xl text-md text-gray-500 flex items-center">
            <button @click="rateQuestionutil(question.uuid, 'upvote')"
              class="mt-3 inline-flex justify-center rounded-md border border-transparent bg-success px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
              Upvote
            </button>
            <button @click="rateQuestionutil(question.uuid, 'downvote')"
              class="mt-3 inline-flex justify-center mx-2 rounded-md border border-transparent bg-danger px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
              Downvote
            </button>
          </div>
        </div>
        <div class="mt-2 max-w-xl text-md text-gray-500">
          <button @click="openModal"
            class="mt-3 inline-flex justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Add Answer
          </button>
        </div>
      </div>
      <div>
        <h3 class="text-xl leading-6 font-medium text-primary my-3">Answers</h3>
        <div class="mt-2 text-md text-gray-500">
          <div v-for="answer in question.answers" :key="answer.id" class="bg-gray-100 p-4 my-2 rounded-lg">
            <p>{{ answer.body }}</p>
            <p>Answered by: {{ answer.author }}</p>
            <p v-if="showUsers(answer.upvoted_users)" class="my-2 bg-success text-white p-2 rounded-lg">
              {{ showUsers(answer.upvoted_users) }} liked this answer
            </p>
            <p v-if="showUsers(answer.downvoted_users)" class="my-2 bg-danger text-white p-2 rounded-lg">
              {{ showUsers(answer.downvoted_users) }} disliked this answer
            </p>
            <div class="flex items-center mt-2">
              <button @click="openCommentModal(answer)"
                class="mt-2 inline-flex justify-center rounded-md border border-transparent bg-success px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                Reply
              </button>
              <button @click="rateAnswerUtil(answer.uuid, 'upvote')"
                class="text-success hover:text-green-900 mx-2 px-2 py-1 rounded-md shadow-lg">
                <PlusIcon class="h-5 w-5" />
              </button>
              <button @click="rateAnswerUtil(answer.uuid, 'downvote')"
                class="text-danger hover:text-red-900 mx-2 px-2 py-1 rounded-md shadow-lg">
                <MinusIcon class="h-5 w-5" />
              </button>
            </div>

            <div class="mt-2 text-md text-gray-500">
              <div class="mt-2 text-md text-gray-500">
                <div v-for="comment in answer.comments" :key="comment.id"
                  class="bg-primary text-white p-2 my-2 rounded-lg">
                  <p>{{ comment.body }}</p>
                  <p class="text-sm">Commented by: {{ comment.author }}</p>

                  <div class="my-2">
                    <button v-if="isCommentOwner(comment)" @click="updateComment(comment)"
                      class="text-blue-600 hover:text-blue-900 mx-2 px-2 py-1 rounded-md shadow-lg">
                      <PencilIcon class="h-5 w-5" />
                    </button>
                    <button v-if="isCommentOwner(comment)" @click="deleteComment(comment.uuid)"
                      class="text-red-600 hover:text-red-900 mx-2 px-2 py-1 rounded-md shadow-lg">
                      <TrashIcon class="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <p v-if="question && question.answers && question.answers.length === 0"
          class="text-center text-lg text-red-800">
          No answers found
        </p>
      </div>
    </section>

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
                <answer-form :closeModal="closeModal" :add-answer="addAnswer" />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <TransitionRoot appear :show="isCommentOpen" as="template">
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
                <comment-form :closeModal="closeCommentModal" :add-comment="addComment" :comment="selectedComment"
                  :update-comment="updateCommentUtil" />
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
import { useRoute } from "vue-router";
import AnswerForm from "../components/AnswerForm.vue";
import CommentForm from "../components/CommentForm.vue";
import Loader from "../components/Loader.vue";
import { useQuestion } from "../store/question";
import { useAnswer } from "../store/answer";
import { useAuth } from "../store/auth";
import { PencilIcon, TrashIcon, PlusIcon, MinusIcon } from "@heroicons/vue/outline";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
} from "@headlessui/vue";

const isOpen = ref(false);
const isCommentOpen = ref(false);
const questionStore = useQuestion();
const answerStore = useAnswer();
const authStore = useAuth();
const selectedAnswer = ref(null);
const selectedComment = ref(null);
const route = useRoute();

const question = computed(() => questionStore.getQuestion);
const isQuestionLoading = computed(() => questionStore.isLoading);

function closeModal() {
  isOpen.value = false;
}

function openModal() {
  isOpen.value = true;
}

function openCommentModal(answer) {
  isCommentOpen.value = true;
  selectedAnswer.value = answer;
}

function closeCommentModal() {
  isCommentOpen.value = false;
  selectedAnswer.value = null;
}

const addAnswer = async (answerBody) => {
  const questionSlug = route.params.slug;
  const payload = {
    body: answerBody,
  };
  await answerStore.addAnswer(questionSlug, payload);
  await questionStore.getQuestionAction(questionSlug);
};

const addComment = async (commentBody) => {
  const questionSlug = route.params.slug;
  const payload = {
    body: commentBody,
    answer: selectedAnswer && selectedAnswer.value.uuid,
  };
  await answerStore.addComment(payload);
  await questionStore.getQuestionAction(questionSlug);
};

const updateCommentUtil = async (commentId, commentBody) => {
  const questionSlug = route.params.slug;
  const payload = {
    body: commentBody,
  };
  await answerStore.updateComment(commentId, payload);
  await questionStore.getQuestionAction(questionSlug);
};

const updateComment = (comment) => {
  selectedComment.value = comment;
  isCommentOpen.value = true;
};

const deleteComment = async (commentId) => {
  const questionSlug = route.params.slug;
  await answerStore.deleteComment(commentId);
  await questionStore.getQuestionAction(questionSlug);
};

const rateQuestionutil = async (questionId, rating) => {
  const payload = {
    rating,
    questionId,
  };
  await questionStore.rateQuestion(payload);
  await questionStore.getQuestionAction(route.params.slug);
};

const rateAnswerUtil = async (answerId, rating) => {
  const payload = {
    rating,
    answerId,
  };
  await answerStore.rateAnswer(payload);
  await questionStore.getQuestionAction(route.params.slug);
};

const showUsersUpvotedByText = computed(() => {
  const upvotedUsers = questionStore.getQuestion.upvoted_users;
  if (upvotedUsers && upvotedUsers.length === 1) {
    return `Liked by ${upvotedUsers[0]}`;
  } else if (upvotedUsers && upvotedUsers.length === 2) {
    return `Liked by ${upvotedUsers[0]} and ${upvotedUsers[1]}`;
  } else if (upvotedUsers && upvotedUsers.length > 2) {
    return `Liked by ${upvotedUsers[0]}, ${upvotedUsers[1]} and ${upvotedUsers.length - 2} others`;
  } else {
    return '';
  }
});

const showUsersDownvotedByText = computed(() => {
  const downvotedUsers = questionStore.getQuestion.downvoted_users;
  if (downvotedUsers && downvotedUsers.length === 1) {
    return `Disliked by ${downvotedUsers[0]}`;
  } else if (downvotedUsers && downvotedUsers.length === 2) {
    return `Disliked by ${downvotedUsers[0]} and ${downvotedUsers[1]}`;
  } else if (downvotedUsers && downvotedUsers.length > 2) {
    return `Disliked by ${downvotedUsers[0]}, ${downvotedUsers[1]} and ${downvotedUsers.length - 2} others`;
  } else {
    return '';
  }
});

const showUsers = (userArray) => {
  if (userArray && userArray.length === 1) {
    return userArray[0];
  } else if (userArray && userArray.length === 2) {
    return `${userArray[0]} and ${userArray[1]}`;
  } else if (userArray && userArray.length > 2) {
    return `${userArray[0]}, ${userArray[1]} and ${userArray.length - 2} others`;
  } else {
    return '';
  }
}

const isCommentOwner = computed(() => {
  return (question) =>
    authStore.authData && question.author === authStore.authData.email;
});

onMounted(async () => {
  const questionSlug = route.params.slug;
  await questionStore.getQuestionAction(questionSlug);
});
</script>
