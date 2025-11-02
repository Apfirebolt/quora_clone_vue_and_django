<template>
  <header-component />
  <main class="bg-white shadow sm:rounded-lg" id="about">
    <section class="px-4 py-5 sm:p-6 container mx-auto">
      <section-header
        :title="question ? question.content : 'Loading Question...'"
        :subtitle="
          question && question.description
            ? question.description
            : 'No description provided'
        "
      />
      <div
        class="flex flex-col lg:flex-row lg:justify-between lg:items-start gap-6 mb-8"
      >
        <Loader v-if="isQuestionLoading" />
        <div class="flex-1">
          <div class="bg-gray-50 p-4 rounded-lg mb-4">
            <p class="text-sm text-gray-600 font-medium">
              Asked by:
              <span class="text-primary font-semibold">{{
                question.author
              }}</span>
            </p>
          </div>

          <div class="space-y-3">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div
                v-if="showUsersUpvotedByText"
                class="flex items-center space-x-3 bg-green-50 border border-green-200 rounded-xl p-4 hover:bg-green-100 transition-colors duration-200"
              >
                <div class="flex-shrink-0">
                  <div
                    class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center"
                  >
                    <PlusIcon class="h-5 w-5 text-white" />
                  </div>
                </div>
                <div class="flex-1">
                  <p class="text-sm font-semibold text-green-800">Upvotes</p>
                  <p class="text-sm text-green-600">
                    {{ showUsersUpvotedByText }}
                  </p>
                </div>
              </div>

              <div
                v-if="showUsersDownvotedByText"
                class="flex items-center space-x-3 bg-red-50 border border-red-200 rounded-xl p-4 hover:bg-red-100 transition-colors duration-200"
              >
                <div class="flex-shrink-0">
                  <div
                    class="w-10 h-10 bg-red-500 rounded-full flex items-center justify-center"
                  >
                    <MinusIcon class="h-5 w-5 text-white" />
                  </div>
                </div>
                <div class="flex-1">
                  <p class="text-sm font-semibold text-red-800">Downvotes</p>
                  <p class="text-sm text-red-600">
                    {{ showUsersDownvotedByText }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="flex flex-wrap gap-3 mt-6">
            <button
              @click="rateQuestionutil(question.uuid, 'upvote')"
              class="inline-flex items-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg shadow-sm transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
            >
              <PlusIcon class="h-4 w-4 mr-2" />
              Upvote
            </button>
            <button
              @click="rateQuestionutil(question.uuid, 'downvote')"
              class="inline-flex items-center px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-medium rounded-lg shadow-sm transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
            >
              <MinusIcon class="h-4 w-4 mr-2" />
              Downvote
            </button>
          </div>
        </div>

        <div class="lg:flex-shrink-0">
          <button
            @click="openModal"
            class="w-full lg:w-auto inline-flex items-center justify-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg shadow-lg transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            <svg
              class="h-5 w-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4v16m8-8H4"
              />
            </svg>
            Add Answer
          </button>
        </div>
      </div>
      <div>
        <h3 class="text-xl leading-6 font-medium text-primary my-3">Answers</h3>
        <div class="mt-2 text-md text-gray-500">
          <div
            v-for="answer in question.answers"
            :key="answer.id"
            class="bg-gray-100 p-4 my-2 rounded-lg"
          >
            <div
              class="bg-white border border-gray-200 rounded-xl p-6 shadow-sm hover:shadow-md transition-all duration-200"
            >
              <!-- Answer Content -->
              <div class="mb-4">
                <p class="text-gray-800 text-base leading-relaxed">
                  {{ answer.body }}
                </p>
              </div>

              <!-- Author Info -->
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center space-x-3">
                  <div
                    class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center"
                  >
                    <span class="text-white text-sm font-semibold">{{
                      answer.author.charAt(0).toUpperCase()
                    }}</span>
                  </div>
                  <div>
                    <p class="text-sm font-medium text-gray-700">
                      {{ answer.author }}
                    </p>
                    <p class="text-xs text-gray-500">Answered</p>
                  </div>
                </div>
              </div>

              <!-- Vote Statistics -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                <div
                  v-if="showUsers(answer.upvoted_users)"
                  class="flex items-center space-x-2 bg-green-50 border border-green-200 rounded-lg p-3"
                >
                  <div
                    class="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center"
                  >
                    <PlusIcon class="h-3 w-3 text-white" />
                  </div>
                  <p class="text-sm text-green-700 font-medium">
                    {{ showUsers(answer.upvoted_users) }} liked this answer
                  </p>
                </div>

                <div
                  v-if="showUsers(answer.downvoted_users)"
                  class="flex items-center space-x-2 bg-red-50 border border-red-200 rounded-lg p-3"
                >
                  <div
                    class="w-6 h-6 bg-red-500 rounded-full flex items-center justify-center"
                  >
                    <MinusIcon class="h-3 w-3 text-white" />
                  </div>
                  <p class="text-sm text-red-700 font-medium">
                    {{ showUsers(answer.downvoted_users) }} disliked this answer
                  </p>
                </div>
              </div>

              <!-- Action Buttons -->
              <div
                class="flex items-center justify-between pt-4 border-t border-gray-100"
              >
                <button
                  @click="openCommentModal(answer)"
                  class="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg shadow-sm transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  <svg
                    class="h-4 w-4 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                    />
                  </svg>
                  Reply
                </button>

                <div class="flex items-center space-x-2">
                  <button
                    @click="rateAnswerUtil(answer.uuid, 'upvote')"
                    class="inline-flex items-center px-3 py-2 bg-green-100 hover:bg-green-200 text-green-700 hover:text-green-800 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                  >
                    <PlusIcon class="h-4 w-4" />
                  </button>
                  <button
                    @click="rateAnswerUtil(answer.uuid, 'downvote')"
                    class="inline-flex items-center px-3 py-2 bg-red-100 hover:bg-red-200 text-red-700 hover:text-red-800 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
                  >
                    <MinusIcon class="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>

            <div
              v-if="answer.comments && answer.comments.length > 0"
              class="mt-4"
            >
              <h4
                class="text-sm font-semibold text-gray-700 mb-3 flex items-center"
              >
                <svg
                  class="h-4 w-4 mr-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                  />
                </svg>
                Comments ({{ answer.comments.length }})
              </h4>
              <div class="space-y-3">
                <div
                  v-for="comment in answer.comments"
                  :key="comment.id"
                  class="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 rounded-xl p-4 shadow-sm hover:shadow-md transition-all duration-200"
                >
                  <div class="flex items-start justify-between">
                    <div class="flex-1">
                      <p class="text-gray-800 text-sm leading-relaxed mb-2">
                        {{ comment.body }}
                      </p>
                      <div
                        class="flex items-center space-x-4 text-xs text-gray-500"
                      >
                        <div class="flex items-center space-x-1">
                          <div
                            class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center"
                          >
                            <span class="text-white text-xs font-semibold">{{
                              comment.author.charAt(0).toUpperCase()
                            }}</span>
                          </div>
                          <span class="font-medium">{{ comment.author }}</span>
                        </div>
                        <div class="flex items-center space-x-1">
                          <svg
                            class="h-3 w-3"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                          </svg>
                          <span>{{ comment.created_at }}</span>
                        </div>
                      </div>
                    </div>

                    <div
                      v-if="isCommentOwner(comment)"
                      class="flex items-center space-x-1 ml-4"
                    >
                      <button
                        @click="updateComment(comment)"
                        class="p-2 text-blue-600 hover:text-blue-800 hover:bg-blue-100 rounded-lg transition-colors duration-200 group"
                        title="Edit comment"
                      >
                        <PencilIcon
                          class="h-4 w-4 group-hover:scale-110 transition-transform"
                        />
                      </button>
                      <button
                        @click="deleteComment(comment.uuid)"
                        class="p-2 text-red-600 hover:text-red-800 hover:bg-red-100 rounded-lg transition-colors duration-200 group"
                        title="Delete comment"
                      >
                        <TrashIcon
                          class="h-4 w-4 group-hover:scale-110 transition-transform"
                        />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <p
          v-if="question && question.answers && question.answers.length === 0"
          class="text-center text-lg text-red-800"
        >
          No answers found
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
                <answer-form :closeModal="closeModal" :add-answer="addAnswer" />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <TransitionRoot appear :show="isCommentOpen" as="template">
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
                <comment-form
                  :closeModal="closeCommentModal"
                  :add-comment="addComment"
                  :comment="selectedComment"
                  :update-comment="updateCommentUtil"
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
import { useRoute } from "vue-router";
import AnswerForm from "../components/AnswerForm.vue";
import CommentForm from "../components/CommentForm.vue";
import Loader from "../components/Loader.vue";
import SectionHeader from "../components/SectionHeader.vue";
import { useQuestion } from "../store/question";
import { useAnswer } from "../store/answer";
import { useAuth } from "../store/auth";
import {
  PencilIcon,
  TrashIcon,
  PlusIcon,
  MinusIcon,
} from "@heroicons/vue/outline";
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
    return `Liked by ${upvotedUsers[0]}, ${upvotedUsers[1]} and ${
      upvotedUsers.length - 2
    } others`;
  } else {
    return "";
  }
});

const showUsersDownvotedByText = computed(() => {
  const downvotedUsers = questionStore.getQuestion.downvoted_users;
  if (downvotedUsers && downvotedUsers.length === 1) {
    return `Disliked by ${downvotedUsers[0]}`;
  } else if (downvotedUsers && downvotedUsers.length === 2) {
    return `Disliked by ${downvotedUsers[0]} and ${downvotedUsers[1]}`;
  } else if (downvotedUsers && downvotedUsers.length > 2) {
    return `Disliked by ${downvotedUsers[0]}, ${downvotedUsers[1]} and ${
      downvotedUsers.length - 2
    } others`;
  } else {
    return "";
  }
});

const showUsers = (userArray) => {
  if (userArray && userArray.length === 1) {
    return userArray[0];
  } else if (userArray && userArray.length === 2) {
    return `${userArray[0]} and ${userArray[1]}`;
  } else if (userArray && userArray.length > 2) {
    return `${userArray[0]}, ${userArray[1]} and ${
      userArray.length - 2
    } others`;
  } else {
    return "";
  }
};

const isCommentOwner = computed(() => {
  return (question) =>
    authStore.authData && question.author === authStore.authData.email;
});

onMounted(async () => {
  const questionSlug = route.params.slug;
  await questionStore.getQuestionAction(questionSlug);
});
</script>
