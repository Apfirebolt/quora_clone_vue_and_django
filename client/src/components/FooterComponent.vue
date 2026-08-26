<template>
  <footer class="border-t border-neutral-800 bg-neutral-950 font-inter text-neutral-400">
    <div class="mx-auto max-w-7xl px-6 py-12 lg:px-8">
      
      <!-- Top Section: Brand & Newsletter Subscription -->
      <div class="grid grid-cols-1 gap-8 pb-12 lg:grid-cols-12 lg:gap-12 border-b border-neutral-800/80">
        <!-- Brand identity -->
        <div class="lg:col-span-5 space-y-4">
          <div class="flex items-center gap-2">
            <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-primary text-white font-bold text-xl shadow-md shadow-red-600/20">
              Q
            </div>
            <span class="text-xl font-bold tracking-tight text-white">Quora Clone</span>
          </div>
          <p class="text-sm leading-relaxed text-neutral-400 max-w-sm">
            A place to share knowledge, understand the world better, and empower people to learn from one another.
          </p>
        </div>

        <!-- Inline Newsletter form -->
        <div class="lg:col-span-7 flex flex-col justify-center">
          <div class="rounded-2xl bg-neutral-900/60 p-6 border border-neutral-800/60 backdrop-blur-sm">
            <h4 class="font-semibold text-primary">Stay in the loop</h4>
            <p class="mt-1 text-sm text-neutral-400">
              Get the weekly digest of the best questions and discussions delivered to your inbox.
            </p>
            <form @submit.prevent="handleSubscribe" class="mt-4 flex flex-col gap-2.5 sm:flex-row sm:items-center">
              <input
                v-model="email"
                type="email"
                required
                placeholder="Enter your email"
                class="w-full min-w-0 rounded-lg border border-neutral-700 bg-neutral-800/50 px-4 py-2.5 text-sm text-white placeholder-neutral-500 transition focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20"
              />
              <button
                type="submit"
                class="inline-flex shrink-0 items-center justify-center rounded-lg bg-red-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/40 active:scale-[0.98]"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>
      </div>

      <!-- Middle Section: Navigation Links -->
      <div class="grid grid-cols-2 gap-8 py-10 sm:grid-cols-4">
        <div>
          <h3 class="text-xs font-semibold uppercase tracking-wider text-neutral-200">Explore</h3>
          <ul class="mt-4 space-y-2.5 text-sm">
            <li><a href="#" class="hover:text-primary transition-colors">Questions</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Spaces</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Topics</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Trending</a></li>
          </ul>
        </div>

        <div>
          <h3 class="text-xs font-semibold uppercase tracking-wider text-neutral-200">Community</h3>
          <ul class="mt-4 space-y-2.5 text-sm">
            <li><a href="#" class="hover:text-primary transition-colors">Guidelines</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Top Writers</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Leaderboard</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Feedback</a></li>
          </ul>
        </div>

        <div>
          <h3 class="text-xs font-semibold uppercase tracking-wider text-neutral-200">Company</h3>
          <ul class="mt-4 space-y-2.5 text-sm">
            <li><a href="#" class="hover:text-primary transition-colors">About</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Careers</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Privacy Policy</a></li>
            <li><a href="#" class="hover:text-primary transition-colors">Terms of Service</a></li>
          </ul>
        </div>

        <div>
          <h3 class="text-xs font-semibold uppercase tracking-wider text-neutral-200">Connect</h3>
          <div class="mt-4 flex gap-3">
            <a href="#" class="flex h-9 w-9 items-center justify-center rounded-lg border border-neutral-800 bg-neutral-900 text-neutral-400 hover:border-neutral-700 hover:text-primary transition" aria-label="Twitter">
              <svg class="h-4 w-4 fill-current" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
            </a>
            <a href="#" class="flex h-9 w-9 items-center justify-center rounded-lg border border-neutral-800 bg-neutral-900 text-neutral-400 hover:border-neutral-700 hover:text-primary transition" aria-label="GitHub">
              <svg class="h-4 w-4 fill-current" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
            </a>
            <a href="#" class="flex h-9 w-9 items-center justify-center rounded-lg border border-neutral-800 bg-neutral-900 text-neutral-400 hover:border-neutral-700 hover:text-primary transition" aria-label="Discord">
              <svg class="h-4 w-4 fill-current" viewBox="0 0 24 24"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994.021-.041.001-.09-.041-.106a13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.929 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.893.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg>
            </a>
          </div>
        </div>
      </div>

      <!-- Bottom Bar: Copyright & System Status -->
      <div class="mt-8 flex flex-col items-center justify-between gap-4 border-t border-neutral-800/80 pt-8 sm:flex-row text-xs">
        <p>© {{ currentYear }} Quora Clone, Inc. All rights reserved.</p>
      </div>

    </div>
  </footer>
</template>

<script>
import { defineComponent, ref, computed } from 'vue'

export default defineComponent({
  setup() {
    const email = ref('')
    const currentYear = computed(() => new Date().getFullYear())

    const handleSubscribe = () => {
      if (!email.value) return
      // Implement newsletter subscription logic
      console.log('Subscribed:', email.value)
      email.value = ''
    }

    return {
      email,
      currentYear,
      handleSubscribe,
    }
  },
})
</script>