<template>
  <div class="flex items-center justify-center p-6" role="status" aria-label="Loading">
    <div class="relative flex items-center justify-center">
      <!-- Background track -->
      <svg
        class="h-10 w-10 animate-spin text-neutral-800"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="3"
        />
        <path
          class="opacity-90 text-red-600"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
        />
      </svg>
      
      <!-- Center subtle glow -->
      <div class="absolute h-2 w-2 rounded-full bg-red-500/30 blur-sm"></div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'AppLoader',
})
</script>