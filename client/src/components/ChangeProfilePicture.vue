<template>
  <form class="space-y-6" @submit="handleSubmit">
    <h2
      class="text-lg text-center font-medium leading-6 text-white bg-primary p-4"
    >
      Change Profile Image
    </h2>

    <div>
      <div class="my-3">
        <img v-if="imagePreview"
          :src="imagePreview"
          alt="Profile Image"
          class="h-42 w-42 rounded-full"
        />
        <p v-else class="text-gray-500">No image selected</p>
      </div>

      <button
        type="button"
        @click="fileInput.click()"
        class="py-2 px-4 mt-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-secondary hover:bg-primary focus:outline-none focus:ring-2 focus:ring-offset-2"
      >
        Choose File
      </button>
      <input
        type="file"
        id="profileImage"
        ref="fileInput"
        @change="handleFileChange"
        class="hidden"
      />
    </div>

    <div v-if="errors.length" class="text-danger">
      <ul>
        <li v-for="error in errors" :key="error">{{ error }}</li>
      </ul>
    </div>

    <div class="text-center">
      <button
        type="submit"
        class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-secondary hover:bg-primary focus:outline-none focus:ring-2 focus:ring-offset-2"
      >
        Update Profile Image
      </button>
      <button
        @click="closeModal"
        class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white mx-2 bg-accent hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2"
      >
        Cancel
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
