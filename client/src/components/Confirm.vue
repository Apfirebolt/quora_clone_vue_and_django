<template>
  <div class="w-full font-inter">
    <div class="relative overflow-hidden rounded-3xl bg-white p-6 sm:p-8 shadow-2xl border border-slate-100">
      
      <!-- Subtle Warning Aura Glow -->
      <div class="pointer-events-none absolute -top-12 left-1/2 -translate-x-1/2 h-32 w-32 rounded-full bg-rose-500/10 blur-2xl"></div>

      <div class="relative space-y-6">
        <!-- Icon & Header Container -->
        <div class="flex flex-col items-center text-center space-y-3">
          <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-rose-50 text-rose-600 ring-8 ring-rose-50/60">
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          </div>

          <div class="space-y-1">
            <h3 class="text-xl font-bold tracking-tight text-slate-900">
              Confirm Action
            </h3>
            <p class="text-xs font-medium uppercase tracking-wider text-slate-400">
              Please review before continuing
            </p>
          </div>
        </div>

        <!-- Message Panel -->
        <div class="rounded-2xl bg-slate-50/80 p-4 text-center border border-slate-100">
          <p class="text-sm font-medium leading-relaxed text-slate-600">
            {{ message }}
          </p>
        </div>

        <!-- Action Buttons -->
        <form @submit.prevent="handleSubmit" class="flex flex-col-reverse sm:flex-row gap-2.5 pt-1">
          <button
            @click="closeModalUtil"
            type="button"
            class="inline-flex w-full items-center justify-center rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 shadow-2xs transition-all hover:bg-slate-50 hover:border-slate-300 focus:outline-none focus:ring-2 focus:ring-slate-300 active:scale-[0.98]"
          >
            Cancel
          </button>

          <button
            type="submit"
            class="inline-flex w-full items-center justify-center rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-accent shadow-sm transition-all hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-primary/40 active:scale-[0.98]"
          >
            Confirm
          </button>
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

const handleSubmit = () => {
  emits("confirmAction");
};

const closeModalUtil = () => {
  emits("cancelAction");
};
</script>