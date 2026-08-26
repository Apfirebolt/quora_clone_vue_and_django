<template>
  <div class="w-full font-inter">
    <div class="relative overflow-hidden rounded-3xl bg-white p-6 sm:p-8 shadow-2xl border border-slate-100">
      
      <!-- Subtle Accent Ambient Glow -->
      <div class="pointer-events-none absolute -top-16 right-0 h-40 w-40 rounded-full bg-primary/10 blur-3xl"></div>

      <!-- Header & Close Button -->
      <div class="relative flex items-center justify-between border-b border-slate-100 pb-5 mb-6">
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-primary/10 text-primary">
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
          </div>
          <div>
            <h2 class="text-xl font-bold tracking-tight text-slate-900">
              Update Profile Photo
            </h2>
            <p class="text-xs text-slate-400">
              Upload a clear picture to personalize your account
            </p>
          </div>
        </div>

        <button
          type="button"
          @click="closeModal"
          class="rounded-xl p-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-600 focus:outline-none focus:ring-2 focus:ring-slate-200"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Form Body -->
      <form class="space-y-6" @submit.prevent="handleSubmit">
        
        <!-- Error Banner -->
        <div
          v-if="errors.length"
          class="flex items-start gap-3 rounded-2xl border border-rose-200 bg-rose-50/70 p-4 text-xs text-rose-800"
        >
          <svg class="h-5 w-5 shrink-0 text-rose-600" viewBox="0 0 20 20" fill="currentColor">
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clip-rule="evenodd"
            />
          </svg>
          <ul class="space-y-0.5 font-semibold">
            <li v-for="error in errors" :key="error">{{ error }}</li>
          </ul>
        </div>

        <!-- Interactive Drag/Click Upload Zone -->
        <div
          @click="fileInput?.click()"
          class="group relative flex flex-col items-center justify-center rounded-3xl border-2 border-dashed border-slate-200 bg-slate-50/60 p-6 text-center transition-all duration-200 hover:border-primary/50 hover:bg-slate-50 cursor-pointer"
        >
          <!-- Image Preview / Empty Avatar Placeholder -->
          <div class="relative mb-3">
            <img
              v-if="imagePreview"
              :src="imagePreview"
              alt="Selected Preview"
              class="h-28 w-28 rounded-3xl object-cover ring-4 ring-white shadow-md transition group-hover:scale-105"
            />
            <div
              v-else
              class="flex h-28 w-28 items-center justify-center rounded-3xl bg-white ring-4 ring-slate-100 shadow-sm transition group-hover:scale-105"
            >
              <svg class="h-10 w-10 text-slate-300 group-hover:text-primary transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                />
              </svg>
            </div>

            <!-- Mini Edit Badge -->
            <div class="absolute -bottom-1 -right-1 flex h-7 w-7 items-center justify-center rounded-xl bg-primary text-accent shadow-sm">
              <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
              </svg>
            </div>
          </div>

          <div class="space-y-1">
            <p class="text-xs sm:text-sm font-semibold text-slate-700 group-hover:text-primary transition-colors">
              {{ imagePreview ? 'Click to replace selected image' : 'Click to select an image from your device' }}
            </p>
            <p class="text-[11px] text-slate-400">
              Supports PNG, JPG, or WebP (max. 5MB)
            </p>
          </div>

          <input
            type="file"
            id="profileImage"
            ref="fileInput"
            @change="handleFileChange"
            accept="image/*"
            class="hidden"
          />
        </div>

        <!-- Action Controls -->
        <div class="flex flex-col-reverse sm:flex-row gap-3 pt-3 border-t border-slate-100">
          <button
            type="button"
            @click="closeModal"
            class="inline-flex flex-1 items-center justify-center rounded-xl border border-slate-200 bg-white px-5 py-2.5 text-sm font-semibold text-slate-700 shadow-2xs transition hover:bg-slate-50 hover:border-slate-300 focus:outline-none focus:ring-2 focus:ring-slate-300 active:scale-[0.98]"
          >
            Cancel
          </button>

          <button
            type="submit"
            class="inline-flex flex-1 items-center justify-center gap-2 rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-accent shadow-sm transition hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-primary/40 active:scale-[0.98]"
          >
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span>Upload Photo</span>
          </button>
        </div>

      </form>
    </div>
  </div>
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
  errors.value = [];
  const file = e.target.files?.[0];
  if (file) {
    imagePreview.value = URL.createObjectURL(file);
  }
};

function handleSubmit() {
  errors.value = [];
  if (!fileInput.value || !fileInput.value.files[0]) {
    errors.value.push("Please select an image file first.");
    return;
  }
  if (props.updateProfileImage) {
    props.updateProfileImage(fileInput.value.files[0]);
  }
}
</script>