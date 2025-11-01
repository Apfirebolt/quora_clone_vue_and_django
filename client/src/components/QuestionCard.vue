<template>
  <div
    class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-gray-200 hover:shadow-lg transition-all duration-300 hover:border-indigo-300"
  >
    <div class="flex justify-between items-start">
      <div class="flex-1 space-y-3">
        <h3
          class="text-lg font-semibold text-gray-900 leading-tight hover:text-indigo-600 transition-colors cursor-pointer"
        >
          {{ question.content }}
        </h3>
        <p class="text-gray-600 leading-relaxed">
          {{ question.description }}
        </p>
        <div class="flex items-center space-x-4 text-sm text-gray-500">
          <span
            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800"
          >
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
</template>

<script setup>
import { ref, onMounted } from "vue";
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
</script>
