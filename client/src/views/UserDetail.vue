<template>
  <header-component />

  <main v-if="user" class="min-h-[calc(100vh-4rem)] bg-neutral/10 py-10 px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-5xl space-y-8">
      
      <Loader v-if="isLoading" />

      <template v-else>
        <!-- Profile Banner Card -->
        <section class="relative overflow-hidden rounded-3xl border border-gray-100 bg-white p-6 sm:p-8 shadow-sm">
          <!-- Subtle Top Gradient -->
          <div class="pointer-events-none absolute -top-16 right-0 h-48 w-48 rounded-full bg-blue-100/50 blur-3xl"></div>

          <div class="relative flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
            <!-- User Info & Avatar -->
            <div class="flex items-center gap-4 sm:gap-6">
              <div
                class="flex h-16 w-16 sm:h-20 sm:w-20 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 text-2xl font-bold text-white shadow-sm ring-4 ring-blue-50"
              >
                {{ (user.firstName || user.username || 'U').charAt(0).toUpperCase() }}
              </div>
              <div class="space-y-1">
                <div class="flex items-center gap-2">
                  <h1 class="text-xl sm:text-2xl font-bold tracking-tight text-gray-900">
                    {{ getFullName(user) }}
                  </h1>
                  <span class="inline-flex items-center rounded-md bg-blue-50 px-2 py-0.5 text-xs font-semibold text-blue-700 ring-1 ring-inset ring-blue-700/10">
                    Member
                  </span>
                </div>
                <p class="text-sm text-gray-500 font-medium">
                  @{{ user.username }}
                </p>
                <p class="text-xs text-gray-400">
                  {{ user.email }}
                </p>
              </div>
            </div>

            <!-- Follow / Unfollow Actions -->
            <div v-if="user.username !== authData?.username" class="flex items-center">
              <button
                v-if="user.followers && user.followers.includes(authData?.email)"
                @click="unfollowUser"
                type="button"
                class="inline-flex items-center justify-center gap-2 rounded-xl border border-rose-200 bg-rose-50 px-5 py-2.5 text-sm font-semibold text-rose-700 transition hover:bg-rose-100 hover:border-rose-300 focus:outline-none focus:ring-2 focus:ring-rose-500/20 active:scale-[0.98]"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7a4 4 0 11-8 0 4 4 0 018 0zM9 14a6 6 0 00-6 6v1h12v-1a6 6 0 00-6-6zM21 12h-6" />
                </svg>
                <span>Unfollow</span>
              </button>

              <button
                v-else
                @click="followUser"
                type="button"
                class="inline-flex items-center justify-center gap-2 rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-accent shadow-sm transition hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-primary/40 active:scale-[0.98]"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
                <span>Follow</span>
              </button>
            </div>
          </div>

          <!-- Quick Stats Row -->
          <div class="mt-8 grid grid-cols-2 sm:grid-cols-4 gap-4 border-t border-gray-100 pt-6">
            <div class="rounded-2xl bg-gray-50/70 p-4 border border-gray-100/80">
              <span class="text-xs font-medium text-gray-500">Questions Asked</span>
              <p class="mt-1 text-2xl font-bold tracking-tight text-blue-600">
                {{ user.questions ? user.questions.length : 0 }}
              </p>
            </div>
            <div class="rounded-2xl bg-gray-50/70 p-4 border border-gray-100/80">
              <span class="text-xs font-medium text-gray-500">Answers Contributed</span>
              <p class="mt-1 text-2xl font-bold tracking-tight text-emerald-600">
                {{ user.answers ? user.answers.length : 0 }}
              </p>
            </div>
            <div class="rounded-2xl bg-gray-50/70 p-4 border border-gray-100/80">
              <span class="text-xs font-medium text-gray-500">Followers</span>
              <p class="mt-1 text-2xl font-bold tracking-tight text-gray-900">
                {{ user.followers ? user.followers.length : 0 }}
              </p>
            </div>
            <div class="rounded-2xl bg-gray-50/70 p-4 border border-gray-100/80">
              <span class="text-xs font-medium text-gray-500">Following</span>
              <p class="mt-1 text-2xl font-bold tracking-tight text-gray-900">
                {{ user.following ? user.following.length : 0 }}
              </p>
            </div>
          </div>
        </section>

        <!-- Social Network Details (Following & Followers) -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Following List -->
          <section class="rounded-3xl border border-gray-100 bg-white p-6 shadow-sm">
            <div class="flex items-center justify-between pb-4 border-b border-gray-100">
              <h3 class="text-base font-semibold text-gray-900">Following</h3>
              <span class="rounded-full bg-blue-50 px-2.5 py-0.5 text-xs font-medium text-blue-700">
                {{ user.following ? user.following.length : 0 }}
              </span>
            </div>
            <div class="mt-4 flex flex-wrap gap-2">
              <span
                v-for="follow in user.following"
                :key="follow"
                class="inline-flex items-center rounded-xl bg-slate-50 border border-slate-200/80 px-3 py-1.5 text-xs font-medium text-slate-700 transition hover:bg-slate-100"
              >
                @{{ follow }}
              </span>
              <p v-if="!user.following || user.following.length === 0" class="text-xs text-gray-400 py-2">
                Not following any members yet.
              </p>
            </div>
          </section>

          <!-- Followers List -->
          <section class="rounded-3xl border border-gray-100 bg-white p-6 shadow-sm">
            <div class="flex items-center justify-between pb-4 border-b border-gray-100">
              <h3 class="text-base font-semibold text-gray-900">Followers</h3>
              <span class="rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-medium text-emerald-700">
                {{ user.followers ? user.followers.length : 0 }}
              </span>
            </div>
            <div class="mt-4 flex flex-wrap gap-2">
              <span
                v-for="follower in user.followers"
                :key="follower"
                class="inline-flex items-center rounded-xl bg-emerald-50/50 border border-emerald-200/60 px-3 py-1.5 text-xs font-medium text-emerald-800 transition hover:bg-emerald-100/50"
              >
                {{ follower }}
              </span>
              <p v-if="!user.followers || user.followers.length === 0" class="text-xs text-gray-400 py-2">
                No followers yet.
              </p>
            </div>
          </section>
        </div>

        <!-- Questions Authored Section -->
        <section class="rounded-3xl border border-gray-100 bg-white p-6 sm:p-8 shadow-sm">
          <div class="flex items-center justify-between pb-6 border-b border-gray-100">
            <div>
              <h2 class="text-lg font-bold tracking-tight text-gray-900">
                Questions Asked
              </h2>
              <p class="text-xs text-gray-500 mt-0.5">
                Browse discussions started by {{ user.firstName || user.username }}
              </p>
            </div>
            <span class="text-xs font-semibold text-gray-400">
              {{ user.questions ? user.questions.length : 0 }} Total
            </span>
          </div>

          <div v-if="user.questions && user.questions.length > 0" class="mt-6 space-y-3">
            <router-link
              v-for="question in user.questions"
              :key="question.id"
              :to="{
                name: 'QuestionDetail',
                params: { slug: question.slug },
              }"
              class="group flex items-center justify-between rounded-2xl border border-slate-200/80 bg-white p-4 transition-all duration-150 hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-sm"
            >
              <div class="flex items-start gap-3 min-w-0 pr-4">
                <span class="mt-0.5 flex h-2 w-2 shrink-0 rounded-full bg-blue-500"></span>
                <p class="text-sm font-medium text-gray-800 group-hover:text-primary transition-colors truncate">
                  {{ question.content }}
                </p>
              </div>
              <span class="text-xs font-semibold text-primary transition-transform group-hover:translate-x-1 shrink-0">
                →
              </span>
            </router-link>
          </div>

          <div
            v-else
            class="mt-6 rounded-2xl border border-dashed border-slate-200 py-10 text-center"
          >
            <p class="text-xs text-gray-400">No questions published yet.</p>
          </div>
        </section>
      </template>

    </div>
  </main>

  <footer-component />
</template>

<script setup>
import { onMounted, computed } from "vue";
import { useUser } from "../store/user";
import { useAuth } from "../store/auth";
import { useRoute } from "vue-router";
import Loader from "../components/Loader.vue";

const userStore = useUser();
const route = useRoute();
const authStore = useAuth();

const user = computed(() => userStore.user);
const authData = computed(() => authStore.authData);

const getFullName = (user) => {
  if (!user) return "";
  if (user.firstName || user.lastName) {
    return `${user.firstName || ""} ${user.lastName || ""}`.trim();
  }
  return user.username;
};

const isLoading = computed(() => userStore.isLoading);

async function followUser() {
  await userStore.followUserAction(user.value.username);
  await userStore.getUserAction(user.value.username);
}

async function unfollowUser() {
  await userStore.unfollowUserAction(user.value.username);
  await userStore.getUserAction(user.value.username);
}

onMounted(async () => {
  const username = route.params.username;
  await userStore.getUserAction(username);
});
</script>