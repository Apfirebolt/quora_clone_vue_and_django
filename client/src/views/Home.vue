<template>
  <header-component />

  <main class="min-h-[calc(100vh-4rem)] bg-neutral/10 py-10 px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-5xl space-y-12">
      
      <!-- Hero Section -->
      <section
        id="about"
        class="relative overflow-hidden rounded-3xl bg-blue-50/80 border border-blue-100 p-8 sm:p-12 md:p-16 text-center shadow-sm backdrop-blur-sm"
      >
        <!-- Subtle Background Glow -->
        <div class="pointer-events-none absolute -top-24 left-1/2 -translate-x-1/2 h-72 w-72 rounded-full bg-blue-200/40 blur-3xl"></div>

        <div class="relative z-10 max-w-2xl mx-auto space-y-6">
          <span class="inline-flex items-center gap-1.5 rounded-full bg-blue-100/80 px-3.5 py-1 text-xs font-semibold tracking-wide text-blue-800 ring-1 ring-inset ring-blue-700/10">
            ✨ Community Knowledge Platform
          </span>

          <h1 class="text-4xl font-extrabold tracking-tight text-blue-900 sm:text-5xl lg:text-6xl">
            Welcome to <span class="text-blue-700">Quora Clone</span>
          </h1>

          <p class="text-base sm:text-lg leading-relaxed text-gray-700">
            A collaborative space to share knowledge, ask burning questions, and better understand the world together.
          </p>

          <div class="flex flex-wrap items-center justify-center gap-4 pt-2">
            <button
              type="button"
              class="inline-flex items-center justify-center rounded-xl bg-black text-white px-6 py-3 text-sm font-semibold shadow-sm transition-all duration-150 hover:bg-secondary hover:shadow active:scale-[0.98]"
            >
              Get Started
            </button>
            <button
              type="button"
              class="inline-flex items-center justify-center rounded-xl bg-accent px-6 py-3 text-sm font-semibold text-primary border border-primary/20 shadow-sm transition-all duration-150 hover:bg-neutral hover:text-accent active:scale-[0.98]"
            >
              Learn More
            </button>
          </div>
        </div>
      </section>

      <!-- Feature Grid Section -->
      <section class="rounded-3xl bg-white p-8 sm:p-10 border border-gray-100 shadow-sm">
        <div class="mb-8">
          <h2 class="text-xl font-bold tracking-tight text-gray-900 sm:text-2xl">
            Platform Capabilities
          </h2>
          <p class="mt-1 text-sm text-gray-500">
            Everything you need to interact, contribute, and discover discussions.
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="feature in features"
            :key="feature.title"
            class="group relative flex items-start gap-3.5 rounded-2xl border border-gray-100 bg-gray-50/50 p-4 transition-all duration-150 hover:border-blue-100 hover:bg-blue-50/40 hover:shadow-sm"
          >
            <span class="mt-1 flex h-2.5 w-2.5 shrink-0 rounded-full bg-secondary ring-4 ring-secondary/20 transition-transform group-hover:scale-110"></span>
            <div>
              <h3 class="text-sm font-semibold text-gray-800 group-hover:text-blue-950">
                {{ feature.title }}
              </h3>
              <p class="text-xs text-gray-500 mt-0.5">
                {{ feature.desc }}
              </p>
            </div>
          </div>
        </div>
      </section>

    </div>
  </main>

  <footer-component />
</template>

<script setup>
const features = [
  { title: 'Add questions', desc: 'Create and post questions to start discussions.' },
  { title: 'Answer questions', desc: 'Share your perspective and provide detailed solutions.' },
  { title: 'Add comments', desc: 'Engage in nested discussions and give quick feedback.' },
  { title: 'Upvote & downvote', desc: 'Curate quality by voting on questions and responses.' },
  { title: 'Authentication', desc: 'Secure register and sign-in workflows with tokens.' },
  { title: 'Authorization', desc: 'Role-based access controls for user operations.' },
  { title: 'Profile management', desc: 'Customize bio, avatar, and view your activity stream.' },
  { title: 'Search & discovery', desc: 'Fast full-text queries across topics and answers.' },
  { title: 'Follow users', desc: 'Keep track of insights from contributors you trust.' },
  { title: 'Account security', desc: 'Change and reset passwords with verified workflows.' },
]
</script>