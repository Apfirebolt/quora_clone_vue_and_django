<template>
  <div class="max-w-xxl mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
    <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-6 py-4">
      <h2 class="text-xl font-semibold text-white text-center">
        {{ props.question ? "Edit Question" : "Add Question" }}
      </h2>
    </div>

    <form class="p-6 space-y-6" @submit="handleSubmit">
      <div
        v-if="errors.length > 0"
        class="bg-red-50 border-l-4 border-red-400 p-4 rounded-md"
      >
        <div class="flex">
          <div class="flex-shrink-0">
            <svg
              class="h-5 w-5 text-red-400"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <div class="ml-3">
            <p
              class="text-sm text-red-700"
              v-for="error in errors"
              :key="error"
            >
              {{ error }}
            </p>
          </div>
        </div>
      </div>

      <div>
        <label
          for="content"
          class="block text-sm font-semibold text-gray-700 mb-2"
        >
          Question Title
        </label>
        <div class="relative">
          <input
            id="content"
            name="content"
            v-model="content"
            type="text"
            placeholder="Enter your question..."
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200 text-gray-700 placeholder-gray-400 shadow-sm"
          />
        </div>
      </div>

      <div>
        <label
          for="description"
          class="block text-sm font-semibold text-gray-700 mb-2"
        >
          Question Description
        </label>
        <div class="relative">
          <textarea
            id="description"
            name="description"
            v-model="description"
            rows="6"
            placeholder="Provide more details about your question..."
            class="w-full px-4 py-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200 text-gray-700 placeholder-gray-400 shadow-sm"
          ></textarea>
          <div class="absolute bottom-3 right-3 text-xs text-gray-400">
            {{ description.length }} characters
          </div>
        </div>
      </div>

      <div class="flex space-x-3 pt-4">
        <button
          type="submit"
          class="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-sm"
        >
          <span class="flex items-center justify-center">
            <svg
              class="w-4 h-4 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 13l4 4L19 7"
              ></path>
            </svg>
            {{ props.question ? "Update Question" : "Post Question" }}
          </span>
        </button>

        <button
          type="button"
          @click="closeModal"
          class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-3 px-4 rounded-lg transition duration-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
        >
          <span class="flex items-center justify-center">
            <svg
              class="w-4 h-4 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
            Cancel
          </span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
const props = defineProps({
  closeModal: {
    type: Function,
    required: true,
  },
  addQuestion: {
    type: Function,
    required: true,
  },
  updateQuestion: {
    type: Function,
    required: false,
  },
  question: {
    type: Object,
    default: null,
    required: false,
  },
});

const content = ref("");
const description = ref("");
const errors = ref([]);
const { closeModal, addQuestion } = props;

function handleSubmit(e) {
  e.preventDefault();
  errors.value = [];
  if (!content.value) {
    errors.value.push("Question is required");
  }
  if (!description.value) {
    errors.value.push("Description is required");
  }
  if (errors.value.length > 0) {
    return;
  } else {
    console.log("Form submitted");
    if (props.question) {
      props.updateQuestion(content.value, description.value);
    } else {
      addQuestion({
        content: content.value,
        description: description.value,
      });
    }
    closeModal();
  }
}

onMounted(() => {
  if (props.question) {
    content.value = props.question.content;
    description.value = props.question.description;
  }
  console.log("Question Form mounted");
});
</script>
