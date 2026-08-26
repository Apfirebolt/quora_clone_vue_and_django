<template>
  <div class="min-h-[70vh] flex items-center justify-center px-4 py-16 sm:px-6 lg:px-8 font-inter">
    <div class="relative w-full max-w-lg text-center">
      
      <!-- Background Ambient Glow -->
      <div class="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-64 w-64 rounded-full bg-red-500/10 blur-3xl"></div>

      <div class="relative z-10 space-y-6">
        <!-- Error Badge -->
        <div class="inline-flex items-center gap-2 rounded-full border border-red-200/80 bg-red-50/80 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-red-700 shadow-xs dark:border-red-900/40 dark:bg-red-950/40 dark:text-red-400">
          <span class="h-1.5 w-1.5 rounded-full bg-red-600 animate-pulse"></span>
          Error 404
        </div>

        <!-- Big Visual Number & Heading -->
        <div>
          <h1 class="text-7xl font-black tracking-tight text-slate-900 sm:text-8xl dark:text-white">
            4<span class="text-red-600">0</span>4
          </h1>
          <h2 class="mt-2 text-xl font-bold tracking-tight text-slate-800 sm:text-2xl dark:text-neutral-200">
            Page Not Found
          </h2>
        </div>

        <!-- Description -->
        <p class="mx-auto max-w-md text-sm sm:text-base leading-relaxed text-slate-600 dark:text-neutral-400">
          The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.
        </p>

        <!-- Action Controls -->
        <div class="flex flex-wrap items-center justify-center gap-3 pt-2">
          <router-link
            to="/"
            class="inline-flex items-center justify-center gap-2 rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-accent shadow-sm transition-all hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-primary/40 active:scale-[0.98]"
          >
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            <span>Back to Homepage</span>
          </router-link>

          <button
            @click="goBack"
            type="button"
            class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-2.5 text-sm font-semibold text-slate-700 shadow-xs transition-all hover:bg-slate-50 hover:border-slate-300 focus:outline-none focus:ring-2 focus:ring-slate-300 active:scale-[0.98] dark:border-neutral-800 dark:bg-neutral-900 dark:text-neutral-300 dark:hover:bg-neutral-800"
          >
            <span>Previous Page</span>
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/')
  }
}
</script>