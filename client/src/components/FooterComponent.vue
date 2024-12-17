<template>
  <footer class="bg-primary py-4">
    <div class="container mx-auto px-4">
      <p class="text-center text-white text-sm">
        &copy; {{ currentYear }} Quora Clone - All rights reserved.
      </p>
    </div>
  </footer>
</template>

<script>
import { defineComponent, computed } from 'vue'

export default defineComponent({
  setup() {
    const currentYear = computed(() => new Date().getFullYear())

    return {
      currentYear,
    }
  },
})
</script>
