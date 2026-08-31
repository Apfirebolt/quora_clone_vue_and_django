<template>
  <div class="w-full font-inter">
    <div class="relative overflow-hidden rounded-3xl bg-white p-6 sm:p-8 shadow-2xl border border-slate-100">
      
      <!-- Ambient Accent Glow -->
      <div class="pointer-events-none absolute -top-16 right-0 h-44 w-44 rounded-full bg-blue-100/50 blur-3xl"></div>

      <!-- Header & Close Button -->
      <div class="relative flex items-center justify-between border-b border-slate-100 pb-5 mb-6">
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-primary/10 text-primary">
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h2 class="text-xl font-bold tracking-tight text-slate-900">
              {{ props.question ? "Edit Question" : "Ask a Question" }}
            </h2>
            <p class="text-xs text-slate-400">
              Provide context and optional attachments to get accurate solutions
            </p>
          </div>
        </div>

        <button
          type="button"
          @click="closeModal"
          class="rounded-xl p-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-600 focus:outline-none focus:ring-2 focus:ring-slate-200"
          aria-label="Close modal"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Form Body -->
      <form class="space-y-5" @submit.prevent="onSubmit">
        
        <!-- Error Alert Banner -->
        <div
          v-if="Object.keys(errors).length > 0 || imageError"
          class="flex items-start gap-3 rounded-2xl border border-rose-200 bg-rose-50/70 p-4 text-xs text-rose-800"
        >
          <svg class="h-5 w-5 shrink-0 text-rose-600" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <div class="space-y-1">
            <p class="font-semibold">Please check the required fields:</p>
            <ul class="list-disc pl-4 space-y-0.5">
              <li v-for="err in Object.values(errors)" :key="err">{{ err }}</li>
              <li v-if="imageError">{{ imageError }}</li>
            </ul>
          </div>
        </div>

        <!-- Question Title Input -->
        <div class="space-y-1.5">
          <label for="content" class="block text-xs font-bold uppercase tracking-wider text-slate-700">
            Question Title <span class="text-rose-500">*</span>
          </label>
          <input
            id="content"
            name="content"
            v-model="content"
            type="text"
            placeholder="e.g. How to properly configure Celery and Redis in Django?"
            class="w-full rounded-xl border bg-slate-50/60 px-4 py-3 text-sm text-slate-900 placeholder-slate-400 transition focus:bg-white focus:outline-none focus:ring-2"
            :class="errors.content ? 'border-rose-400 focus:border-rose-500 focus:ring-rose-500/20' : 'border-slate-200 focus:border-primary focus:ring-primary/20'"
          />
          <p v-if="errors.content" class="text-xs font-medium text-rose-600">
            {{ errors.content }}
          </p>
        </div>

        <!-- Question Description Input -->
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <label for="description" class="block text-xs font-bold uppercase tracking-wider text-slate-700">
              Details & Context <span class="text-rose-500">*</span>
            </label>
            <span class="text-[11px] font-medium text-slate-400">
              {{ description?.length || 0 }} characters
            </span>
          </div>
          <textarea
            id="description"
            name="description"
            v-model="description"
            rows="4"
            placeholder="Describe your issue, paste relevant logs, or mention what you've tried..."
            class="w-full rounded-xl border bg-slate-50/60 px-4 py-3 text-sm text-slate-900 placeholder-slate-400 transition resize-none focus:bg-white focus:outline-none focus:ring-2"
            :class="errors.description ? 'border-rose-400 focus:border-rose-500 focus:ring-rose-500/20' : 'border-slate-200 focus:border-primary focus:ring-primary/20'"
          ></textarea>
          <p v-if="errors.description" class="text-xs font-medium text-rose-600">
            {{ errors.description }}
          </p>
        </div>

        <!-- Optional Image Upload Section -->
        <div class="space-y-1.5">
          <label class="block text-xs font-bold uppercase tracking-wider text-slate-700">
            Attach Image <span class="text-slate-400 text-2xs normal-case font-normal">(Optional, max 5 MB)</span>
          </label>

          <!-- Selected / Existing Image Preview Box -->
          <div
            v-if="imagePreview"
            class="relative rounded-2xl border border-slate-200 overflow-hidden bg-slate-900/5 group"
          >
            <img
              :src="imagePreview"
              alt="Question snapshot preview"
              class="w-full h-44 object-cover"
            />
            <div class="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
              <button
                type="button"
                @click="triggerFileInput"
                class="px-3 py-1.5 rounded-lg bg-white/90 text-slate-900 text-xs font-semibold shadow hover:bg-white transition"
              >
                Replace
              </button>
              <button
                type="button"
                @click="removeImage"
                class="px-3 py-1.5 rounded-lg bg-rose-600 text-white text-xs font-semibold shadow hover:bg-rose-700 transition"
              >
                Remove
              </button>
            </div>
          </div>

          <!-- Empty Upload Dropzone -->
          <div
            v-else
            @click="triggerFileInput"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="onDropFile"
            class="border-2 border-dashed rounded-2xl p-6 text-center cursor-pointer transition-all flex flex-col items-center justify-center gap-2"
            :class="isDragging ? 'border-primary bg-primary/5' : 'border-slate-200 bg-slate-50/50 hover:bg-slate-50 hover:border-slate-300'"
          >
            <div class="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="text-xs">
              <span class="font-semibold text-primary hover:underline">Click to upload</span> or drag and drop
            </div>
            <p class="text-[11px] text-slate-400">PNG, JPG, or WEBP (up to 5MB)</p>
          </div>

          <!-- Hidden Native File Input -->
          <input
            ref="fileInputRef"
            type="file"
            accept="image/png, image/jpeg, image/webp"
            class="hidden"
            @change="onFileSelected"
          />
        </div>

        <!-- Action Buttons -->
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
            class="inline-flex flex-1 items-center justify-center gap-2 rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-primary/40 active:scale-[0.98]"
          >
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span>{{ props.question ? "Save Changes" : "Publish Question" }}</span>
          </button>
        </div>

      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useForm } from "vee-validate";
import * as yup from "yup";

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

const fileInputRef = ref(null);
const selectedFile = ref(null);
const imagePreview = ref(null);
const imageError = ref(null);
const isDragging = ref(false);

const validationSchema = yup.object({
  content: yup
    .string()
    .required("Question title is required")
    .min(10, "Title must be at least 10 characters long"),
  description: yup
    .string()
    .required("Description is required")
    .min(20, "Description must be at least 20 characters long"),
});

const { errors, handleSubmit, defineField } = useForm({
  validationSchema,
});

const [content] = defineField("content");
const [description] = defineField("description");

const triggerFileInput = () => {
  fileInputRef.value?.click();
};

const validateAndSetFile = (file) => {
  imageError.value = null;

  if (!file) return;

  const validTypes = ["image/jpeg", "image/png", "image/webp"];
  if (!validTypes.includes(file.type)) {
    imageError.value = "Only JPG, PNG, and WEBP image files are allowed.";
    return;
  }

  const maxSizeInBytes = 5 * 1024 * 1024; // 5 MB
  if (file.size > maxSizeInBytes) {
    imageError.value = "Image size exceeds 5MB limit.";
    return;
  }

  selectedFile.value = file;
  imagePreview.value = URL.createObjectURL(file);
};

const onFileSelected = (event) => {
  const file = event.target.files?.[0];
  validateAndSetFile(file);
};

const onDropFile = (event) => {
  isDragging.value = false;
  const file = event.dataTransfer?.files?.[0];
  validateAndSetFile(file);
};

const removeImage = () => {
  selectedFile.value = null;
  imagePreview.value = null;
  imageError.value = null;
  if (fileInputRef.value) {
    fileInputRef.value.value = "";
  }
};

const onSubmit = handleSubmit(async (values) => {
  const payload = {
    content: values.content,
    description: values.description,
  };

  if (selectedFile.value) {
    payload.image = selectedFile.value;
  }

  if (props.question) {
    await props.updateQuestion(props.question.slug, payload);
  } else {
    await props.addQuestion(payload);
  }

  props.closeModal();
});

onMounted(() => {
  if (props.question) {
    content.value = props.question.content || "";
    description.value = props.question.description || "";
    if (props.question.image_url || props.question.image) {
      imagePreview.value = props.question.image_url || props.question.image;
    }
  }
});
</script>