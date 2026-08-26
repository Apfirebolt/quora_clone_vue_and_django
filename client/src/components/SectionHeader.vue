<template>
  <div class="space-y-1.5 font-inter">
    <!-- Title with Brand-Themed Accent Dot -->
    <div class="flex items-center gap-2">
      <span class="h-2 w-2 rounded-full bg-primary ring-4 ring-primary/20"></span>
      <h2 class="text-xl sm:text-2xl font-bold tracking-tight text-neutral-900 dark:text-white">
        {{ title }}
      </h2>
    </div>

    <!-- Subtitle -->
    <p
      v-if="subtitle"
      class="text-xs sm:text-sm text-slate-500 dark:text-neutral-400 max-w-2xl leading-relaxed"
    >
      {{ subtitle }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    required: false,
    default: "",
  },
});
</script>