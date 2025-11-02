<template>
  <div
    class="flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Confirmation
        </h2>
      </div>
      <div class="bg-white shadow-md rounded-lg px-8 pt-6 pb-8">
        <form @submit="handleSubmit" class="space-y-6">
          <div class="mb-4">
            <p class="text-gray-700 text-sm font-medium mb-4">
              {{ message }}
            </p>
          </div>
          <div class="flex items-center justify-between space-x-4">
            <button
              type="submit"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Confirm
            </button>
            <button
              @click="closeModalUtil"
              type="button"
              class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  message: {
    type: String,
    required: true,
  },
});

const emits = defineEmits(["confirmAction", "cancelAction"]);

const handleSubmit = async (e) => {
  e.preventDefault();
  emits("confirmAction");
};

const closeModalUtil = () => {
  emits("cancelAction");
};
</script>
