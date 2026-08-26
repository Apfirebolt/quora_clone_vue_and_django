<template>
  <div class="w-full font-inter">
    <div class="relative overflow-hidden rounded-3xl bg-white p-6 sm:p-8 shadow-2xl border border-slate-100">
      
      <!-- Ambient Backdrop Glow -->
      <div class="pointer-events-none absolute -top-16 right-0 h-44 w-44 rounded-full bg-blue-100/50 blur-3xl"></div>

      <!-- Header & Close Button -->
      <div class="relative flex items-center justify-between border-b border-slate-100 pb-5 mb-6">
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-primary/10 text-primary">
            <!-- Comment Bubble Icon -->
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <div>
            <h2 class="text-xl font-bold tracking-tight text-slate-900">
              {{ comment ? "Edit Comment" : "Add Comment" }}
            </h2>
            <p class="text-xs text-slate-400">
              Join the conversation and share your thoughts
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
      <form class="space-y-5" @submit="handleSubmit">
        
        <!-- Error Banner -->
        <div
          v-if="errors.length > 0"
          class="flex items-start gap-3 rounded-2xl border border-rose-200 bg-rose-50/70 p-4 text-xs text-rose-800"
        >
          <svg class="h-5 w-5 shrink-0 text-rose-600" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <div class="space-y-0.5">
            <p class="font-semibold" v-for="error in errors" :key="error">{{ error }}</p>
          </div>
        </div>

        <!-- Textarea Field -->
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <label for="body" class="block text-xs font-bold uppercase tracking-wider text-slate-700">
              Your Comment <span class="text-rose-500">*</span>
            </label>
            <span class="text-[11px] font-medium text-slate-400">
              {{ body.length }} characters
            </span>
          </div>
          <div class="relative">
            <textarea
              id="body"
              name="body"
              v-model="body"
              rows="4"
              placeholder="Write a clear, constructive comment..."
              class="w-full rounded-xl border bg-slate-50/60 px-4 py-3 text-sm text-slate-900 placeholder-slate-400 transition resize-none focus:bg-white focus:outline-none focus:ring-2"
              :class="errors.length > 0 ? 'border-rose-400 focus:border-rose-500 focus:ring-rose-500/20' : 'border-slate-200 focus:border-primary focus:ring-primary/20'"
            ></textarea>
          </div>
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
            class="inline-flex flex-1 items-center justify-center gap-2 rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-accent shadow-sm transition hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-primary/40 active:scale-[0.98]"
          >
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span>{{ comment ? "Update" : "Post" }}</span>
          </button>
        </div>

      </form>
    </div>
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
    body.value = props.comment.body || "";
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