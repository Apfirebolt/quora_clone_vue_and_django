<template>
  <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-md">
    <form class="space-y-6 p-6" @submit="handleSubmit">
      <h2 class="text-xl font-semibold text-gray-800 text-center border-b pb-4">
        {{ comment ? "Edit Comment" : "Add Comment" }}
      </h2>

      <!-- Error Display -->
      <div v-if="errors.length > 0" class="bg-red-50 border border-red-200 rounded-md p-3">
        <ul class="text-red-600 text-sm">
          <li v-for="error in errors" :key="error">{{ error }}</li>
        </ul>
      </div>

      <div>
        <label for="body" class="block text-sm font-medium text-gray-700 mb-2">
          Your Comment
        </label>
        <textarea
          id="body"
          v-model="body"
          rows="4"
          placeholder="Write your comment here..."
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
          :class="{ 'border-red-500': errors.length > 0 }"
        />
      </div>

      <div class="flex justify-end space-x-3 pt-4 border-t">
        <button
          type="button"
          @click="closeModal"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500"
        >
          Cancel
        </button>
        <button
          type="submit"
          class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {{ comment ? "Update Comment" : "Post Comment" }}
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
  addComment: {
    type: Function,
    required: false,
  },
  updateComment: {
    type: Function,
    required: false,
  },
  comment: {
    type: Object,
    required: false,
    default: null,
  },
});

const body = ref("");
const errors = ref([]);

onMounted(() => {
  if (props.comment) {
    body.value = props.comment.body;
  }
});

function handleSubmit(e) {
  e.preventDefault();
  errors.value = [];
  
  if (!body.value.trim()) {
    errors.value.push("Comment body is required");
    return;
  }
  
  if (props.comment && props.updateComment) {
    props.updateComment(props.comment.uuid, body.value.trim());
  } else if (props.addComment) {
    props.addComment(body.value.trim());
  }
  
  props.closeModal();
}
</script>
