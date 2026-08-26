<template>
  <header-component />

  <main class="min-h-[calc(100vh-4rem)] bg-neutral/10 py-10 px-4 sm:px-6 lg:px-8 font-inter" id="about">
    <div class="mx-auto max-w-5xl space-y-8">
      
      <Loader v-if="isQuestionLoading" />

      <template v-else-if="question">
        <!-- Question Main Card -->
        <article class="relative overflow-hidden rounded-3xl border border-gray-100 bg-white p-6 sm:p-8 shadow-sm">
          <!-- Subtle Backdrop Gradient -->
          <div class="pointer-events-none absolute -top-20 right-0 h-48 w-48 rounded-full bg-blue-100/40 blur-3xl"></div>

          <div class="relative space-y-6">
            <!-- Author Meta & Add Answer Action -->
            <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-gray-100 pb-5">
              <div class="flex items-center gap-3">
                <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 text-sm font-bold text-white shadow-sm ring-4 ring-blue-50">
                  {{ (question.author || 'U').charAt(0).toUpperCase() }}
                </div>
                <div>
                  <p class="text-xs text-gray-400 font-medium">Asked by</p>
                  <span class="text-sm font-semibold text-primary">
                    {{ question.author }}
                  </span>
                </div>
              </div>

              <!-- Top Add Answer Button -->
              <button
                @click="openModal"
                type="button"
                class="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-accent shadow-sm transition hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-primary/40 active:scale-[0.98]"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
                </svg>
                <span>Write Answer</span>
              </button>
            </div>

            <!-- Question Heading & Description -->
            <div class="space-y-3">
              <h1 class="text-xl sm:text-2xl lg:text-3xl font-bold tracking-tight text-gray-900 leading-snug">
                {{ question.content }}
              </h1>
              <p class="text-sm sm:text-base leading-relaxed text-gray-600">
                {{ question.description || 'No description provided' }}
              </p>
            </div>

            <!-- Question Voting & Dynamic Feedback Pill Badges -->
            <div class="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-gray-100">
              <!-- Voting Buttons -->
              <div class="inline-flex items-center rounded-xl bg-slate-50 p-1 border border-slate-200/80">
                <button
                  @click="rateQuestionutil(question.uuid, 'upvote')"
                  type="button"
                  class="inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold text-emerald-700 hover:bg-white hover:shadow-xs transition focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                  title="Upvote Question"
                >
                  <PlusIcon class="h-3.5 w-3.5 stroke-[2.5]" />
                  <span>Upvote</span>
                </button>
                <div class="h-4 w-[1px] bg-slate-200 mx-1"></div>
                <button
                  @click="rateQuestionutil(question.uuid, 'downvote')"
                  type="button"
                  class="inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold text-rose-700 hover:bg-white hover:shadow-xs transition focus:outline-none focus:ring-2 focus:ring-rose-500/20"
                  title="Downvote Question"
                >
                  <MinusIcon class="h-3.5 w-3.5 stroke-[2.5]" />
                  <span>Downvote</span>
                </button>
              </div>

              <!-- Vote Summaries -->
              <div class="flex flex-wrap items-center gap-2 text-xs">
                <span
                  v-if="showUsersUpvotedByText"
                  class="inline-flex items-center gap-1.5 rounded-lg bg-emerald-50 border border-emerald-200/70 px-2.5 py-1 font-medium text-emerald-700"
                >
                  <span class="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
                  {{ showUsersUpvotedByText }}
                </span>
                <span
                  v-if="showUsersDownvotedByText"
                  class="inline-flex items-center gap-1.5 rounded-lg bg-rose-50 border border-rose-200/70 px-2.5 py-1 font-medium text-rose-700"
                >
                  <span class="h-1.5 w-1.5 rounded-full bg-rose-500"></span>
                  {{ showUsersDownvotedByText }}
                </span>
              </div>
            </div>
          </div>
        </article>

        <!-- Answers Section -->
        <section class="space-y-6">
          <div class="flex items-center justify-between px-1">
            <h2 class="text-lg font-bold tracking-tight text-gray-900">
              Answers <span class="text-primary font-medium text-base">({{ question.answers ? question.answers.length : 0 }})</span>
            </h2>
          </div>

          <!-- Answer Cards Loop -->
          <div v-if="question.answers && question.answers.length > 0" class="space-y-6">
            <article
              v-for="answer in question.answers"
              :key="answer.id"
              class="rounded-3xl border border-slate-200/80 bg-white p-6 sm:p-7 shadow-sm transition-all hover:border-slate-300"
            >
              <!-- Author Row -->
              <div class="flex items-center justify-between pb-4 border-b border-gray-100">
                <div class="flex items-center gap-3">
                  <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-900 text-xs font-bold text-white shadow-xs">
                    {{ answer.author.charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <h3 class="text-sm font-semibold text-gray-900 leading-tight">
                      {{ answer.author }}
                    </h3>
                    <p class="text-xs text-gray-400">Contributed answer</p>
                  </div>
                </div>
              </div>

              <!-- Answer Body -->
              <p class="mt-4 text-sm sm:text-base leading-relaxed text-gray-700 whitespace-pre-line">
                {{ answer.body }}
              </p>

              <!-- Answer Feedback Pills -->
              <div v-if="showUsers(answer.upvoted_users) || showUsers(answer.downvoted_users)" class="mt-4 flex flex-wrap gap-2">
                <span
                  v-if="showUsers(answer.upvoted_users)"
                  class="inline-flex items-center gap-1.5 rounded-md bg-emerald-50 border border-emerald-200/60 px-2 py-0.5 text-xs font-medium text-emerald-700"
                >
                  👍 {{ showUsers(answer.upvoted_users) }} liked this
                </span>
                <span
                  v-if="showUsers(answer.downvoted_users)"
                  class="inline-flex items-center gap-1.5 rounded-md bg-rose-50 border border-rose-200/60 px-2 py-0.5 text-xs font-medium text-rose-700"
                >
                  👎 {{ showUsers(answer.downvoted_users) }} disliked this
                </span>
              </div>

              <!-- Answer Footer Action Bar -->
              <div class="mt-5 flex items-center justify-between border-t border-gray-100 pt-4">
                <!-- Reply Button -->
                <button
                  @click="openCommentModal(answer)"
                  type="button"
                  class="inline-flex items-center gap-1.5 rounded-xl border border-gray-200 bg-white px-3.5 py-1.5 text-xs font-semibold text-gray-700 transition hover:bg-gray-50 hover:border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary/30"
                >
                  <svg class="h-3.5 w-3.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                  <span>Reply</span>
                </button>

                <!-- Answer Segmented Votes -->
                <div class="flex items-center gap-1 rounded-xl bg-slate-50 p-1 border border-slate-100">
                  <button
                    @click="rateAnswerUtil(answer.uuid, 'upvote')"
                    type="button"
                    class="inline-flex h-7 w-7 items-center justify-center rounded-lg text-slate-500 transition hover:bg-white hover:text-emerald-600 hover:shadow-xs focus:outline-none"
                    title="Upvote Answer"
                  >
                    <PlusIcon class="h-3.5 w-3.5 stroke-[2.5]" />
                  </button>
                  <button
                    @click="rateAnswerUtil(answer.uuid, 'downvote')"
                    type="button"
                    class="inline-flex h-7 w-7 items-center justify-center rounded-lg text-slate-500 transition hover:bg-white hover:text-rose-600 hover:shadow-xs focus:outline-none"
                    title="Downvote Answer"
                  >
                    <MinusIcon class="h-3.5 w-3.5 stroke-[2.5]" />
                  </button>
                </div>
              </div>

              <!-- Nested Comments Section -->
              <div v-if="answer.comments && answer.comments.length > 0" class="mt-6 rounded-2xl bg-gray-50/70 p-4 sm:p-5 border border-gray-100">
                <div class="flex items-center gap-2 mb-3">
                  <span class="text-xs font-bold uppercase tracking-wider text-gray-500">
                    Comments ({{ answer.comments.length }})
                  </span>
                </div>

                <div class="space-y-2.5">
                  <div
                    v-for="comment in answer.comments"
                    :key="comment.id"
                    class="group flex items-start justify-between rounded-xl bg-white p-3.5 border border-gray-200/70 shadow-2xs"
                  >
                    <div class="space-y-1.5 flex-1 min-w-0 pr-3">
                      <p class="text-xs sm:text-sm text-gray-800 leading-relaxed">
                        {{ comment.body }}
                      </p>
                      <div class="flex items-center gap-2 text-[11px] text-gray-400">
                        <span class="font-semibold text-gray-700">{{ comment.author }}</span>
                        <span>•</span>
                        <span>{{ comment.created_at }}</span>
                      </div>
                    </div>

                    <!-- Owner Controls -->
                    <div v-if="isCommentOwner(comment)" class="flex items-center gap-1 shrink-0">
                      <button
                        @click="updateComment(comment)"
                        type="button"
                        class="p-1 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition"
                        title="Edit comment"
                      >
                        <PencilIcon class="h-3.5 w-3.5" />
                      </button>
                      <button
                        @click="deleteComment(comment.uuid)"
                        type="button"
                        class="p-1 text-gray-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition"
                        title="Delete comment"
                      >
                        <TrashIcon class="h-3.5 w-3.5" />
                      </button>
                    </div>
                  </div>
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
            <h3 class="mt-4 text-sm font-semibold text-slate-900">No answers yet</h3>
            <p class="mt-1 text-sm text-slate-500">
              Be the first to share your knowledge on this topic.
            </p>
          </div>
        </section>
      </template>

    </div>

    <!-- Modals -->
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
                <answer-form :closeModal="closeModal" :add-answer="addAnswer" />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <TransitionRoot appear :show="isCommentOpen" as="template">
      <Dialog as="div" @close="closeCommentModal" class="relative z-50">
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
              <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-3xl bg-white p-6 sm:p-8 text-left align-middle shadow-2xl border border-slate-100 transition-all">
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
  selectedComment.value = null;
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
    answer: selectedAnswer.value ? selectedAnswer.value.uuid : null,
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
  const upvotedUsers = questionStore.getQuestion?.upvoted_users;
  if (!upvotedUsers || upvotedUsers.length === 0) return "";
  if (upvotedUsers.length === 1) return `Liked by ${upvotedUsers[0]}`;
  if (upvotedUsers.length === 2) return `Liked by ${upvotedUsers[0]} and ${upvotedUsers[1]}`;
  return `Liked by ${upvotedUsers[0]}, ${upvotedUsers[1]} and ${upvotedUsers.length - 2} others`;
});

const showUsersDownvotedByText = computed(() => {
  const downvotedUsers = questionStore.getQuestion?.downvoted_users;
  if (!downvotedUsers || downvotedUsers.length === 0) return "";
  if (downvotedUsers.length === 1) return `Disliked by ${downvotedUsers[0]}`;
  if (downvotedUsers.length === 2) return `Disliked by ${downvotedUsers[0]} and ${downvotedUsers[1]}`;
  return `Disliked by ${downvotedUsers[0]}, ${downvotedUsers[1]} and ${downvotedUsers.length - 2} others`;
});

const showUsers = (userArray) => {
  if (!userArray || userArray.length === 0) return "";
  if (userArray.length === 1) return userArray[0];
  if (userArray.length === 2) return `${userArray[0]} and ${userArray[1]}`;
  return `${userArray[0]}, ${userArray[1]} and ${userArray.length - 2} others`;
};

const isCommentOwner = computed(() => {
  return (comment) =>
    authStore.authData && comment.author === authStore.authData.email;
});

onMounted(async () => {
  const questionSlug = route.params.slug;
  await questionStore.getQuestionAction(questionSlug);
});
</script>