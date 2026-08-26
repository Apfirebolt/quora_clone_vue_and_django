<template>
  <article
    class="group relative rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-md dark:border-neutral-800 dark:bg-neutral-900"
  >
    <div class="flex flex-col gap-4">
      
      <!-- Top Header: Author info & Action buttons -->
      <div class="flex items-center justify-between gap-4">
        <!-- Author Metadata -->
        <div class="flex items-center gap-3">
          <!-- Avatar fallback -->
          <div
            class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-indigo-500 to-indigo-700 text-xs font-semibold text-white shadow-sm ring-2 ring-indigo-500/20"
          >
            {{ (question.author || 'U').charAt(0).toUpperCase() }}
          </div>
          <div class="flex flex-col">
            <span class="text-sm font-semibold text-slate-800 dark:text-neutral-200">
              {{ question.author }}
            </span>
            <div class="flex items-center gap-2 text-xs text-slate-400 dark:text-neutral-500">
              <time :datetime="question.created_at">
                {{ formattedDate }}
              </time>
              <span>•</span>
              <span class="inline-flex items-center text-slate-400">Question</span>
            </div>
          </div>
        </div>

        <!-- Quick Actions Toolbar -->
        <div class="flex items-center gap-1 rounded-xl bg-slate-50 p-1 border border-slate-100 dark:bg-neutral-800/60 dark:border-neutral-800">
          <button
            @click="viewQuestion(question)"
            class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 transition-colors hover:bg-white hover:text-indigo-600 hover:shadow-xs focus:outline-none focus:ring-2 focus:ring-indigo-500/20 dark:text-neutral-400 dark:hover:bg-neutral-700 dark:hover:text-neutral-100"
            title="View full question"
          >
            <EyeIcon class="h-4 w-4" />
          </button>

          <template v-if="isQuestionOwner(question)">
            <button
              @click="updateQuestion(question)"
              class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 transition-colors hover:bg-white hover:text-blue-600 hover:shadow-xs focus:outline-none focus:ring-2 focus:ring-blue-500/20 dark:text-neutral-400 dark:hover:bg-neutral-700 dark:hover:text-neutral-100"
              title="Edit question"
            >
              <PencilIcon class="h-4 w-4" />
            </button>

            <button
              @click="deleteQuestion(question)"
              class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 transition-colors hover:bg-white hover:text-rose-600 hover:shadow-xs focus:outline-none focus:ring-2 focus:ring-rose-500/20 dark:text-neutral-400 dark:hover:bg-neutral-700 dark:hover:text-rose-400"
              title="Delete question"
            >
              <TrashIcon class="h-4 w-4" />
            </button>
          </template>
        </div>
      </div>

      <!-- Main Body: Title and clamped description -->
      <div class="space-y-2">
        <h3
          @click="viewQuestion(question)"
          class="cursor-pointer text-lg font-semibold tracking-tight text-slate-900 transition-colors hover:text-indigo-600 dark:text-neutral-100 dark:hover:text-indigo-400"
        >
          {{ question.content }}
        </h3>
        <p class="line-clamp-3 text-sm leading-relaxed text-slate-600 dark:text-neutral-400">
          {{ question.description }}
        </p>
      </div>

      <!-- Bottom Interactive Bar -->
      <div class="flex items-center justify-between pt-2 border-t border-slate-100 dark:border-neutral-800/80">
        <button
          @click="viewQuestion(question)"
          class="group/btn inline-flex items-center gap-1.5 text-xs font-semibold text-indigo-600 transition hover:text-indigo-700 dark:text-indigo-400"
        >
          <span>Read answers</span>
          <span class="transition-transform group-hover/btn:translate-x-0.5">→</span>
        </button>
      </div>

    </div>
  </article>
</template>

<script setup>
import { computed } from "vue";
import { PencilIcon, TrashIcon, EyeIcon } from "@heroicons/vue/outline";

const props = defineProps({
  question: {
    type: Object,
    required: true,
  },
  deleteQuestion: {
    type: Function,
    required: true,
  },
  updateQuestion: {
    type: Function,
    required: true,
  },
  viewQuestion: {
    type: Function,
    required: true,
  },
  isQuestionOwner: {
    type: Function,
    required: true,
  },
});

const formattedDate = computed(() => {
  if (!props.question?.created_at) return "";
  return new Date(props.question.created_at).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
});
</script>