<template>
  <form
    class="bg-white rounded-lg shadow-xl max-w-md mx-auto"
    @submit="handleSubmit"
  >
    <div class="px-6 py-4 border-b border-gray-200">
      <h2 class="text-xl font-semibold text-gray-800">Change Profile Image</h2>
    </div>

    <div class="px-6 py-6">
      <div class="flex flex-col items-center mb-6">
        <div class="relative mb-4">
          <img
            v-if="imagePreview"
            :src="imagePreview"
            alt="Profile Image"
            class="h-32 w-32 rounded-full object-cover border-4 border-gray-200 shadow-md"
          />
          <div
            v-else
            class="h-32 w-32 rounded-full bg-gray-100 border-4 border-gray-200 flex items-center justify-center"
          >
            <svg
              class="h-12 w-12 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
          </div>
        </div>

        <button
          type="button"
          @click="fileInput.click()"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
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
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
          Choose Image
        </button>
        <input
          type="file"
          id="profileImage"
          ref="fileInput"
          @change="handleFileChange"
          accept="image/*"
          class="hidden"
        />
      </div>

      <div
        v-if="errors.length"
        class="mb-4 p-3 bg-red-50 border border-red-200 rounded-md"
      >
        <div class="flex">
          <svg
            class="h-5 w-5 text-red-400"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clip-rule="evenodd"
            />
          </svg>
          <div class="ml-3">
            <ul class="text-sm text-red-700">
              <li v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div
      class="px-6 py-4 bg-gray-50 border-t border-gray-200 rounded-b-lg flex justify-end space-x-3"
    >
      <button
        type="button"
        @click="closeModal"
        class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
      >
        Cancel
      </button>
      <button
        type="submit"
        class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Update Image
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref } from "vue";
const props = defineProps({
  closeModal: {
    type: Function,
    required: true,
  },
  updateProfileImage: {
    type: Function,
    required: false,
  },
});

const errors = ref([]);
const fileInput = ref(null);
const imagePreview = ref("");
const { closeModal } = props;

const handleFileChange = (e) => {
  const file = e.target.files[0];
  if (file) {
    imagePreview.value = URL.createObjectURL(file);
  }
};

function handleSubmit(e) {
  e.preventDefault();
  errors.value = [];
  if (!fileInput.value || !fileInput.value.files[0]) {
    errors.value.push("Please select a file.");
    return;
  }
  // Proceed with form submission logic
  if (props.updateProfileImage) {
    props.updateProfileImage(fileInput.value.files[0]);
  }
}
</script>
