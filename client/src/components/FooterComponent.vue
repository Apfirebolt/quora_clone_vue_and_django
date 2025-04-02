<template>
  <footer class="bg-neutral text-accent py-4 font-inter">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-center text-white">
        <div>
          <h3 class="text-lg font-semibold">Ask Questions</h3>
          <p class="text-sm">
            Post your questions and get answers from the community.
          </p>
        </div>
        <div>
          <h3 class="text-lg font-semibold">Get Answers</h3>
          <p class="text-sm">
            Receive insightful answers from experts and enthusiasts.
          </p>
        </div>
        <div>
          <h3 class="text-lg font-semibold">Engage</h3>
          <p class="text-sm">
            Interact with others by upvoting, commenting, and sharing.
          </p>
        </div>
      </div>
      <div class="mt-4 text-center">
        <button class="bg-primary mb-5 text-white py-2 px-4 rounded hover:bg-primary-dark">
          Subscribe to Newsletter
        </button>
      </div>
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
