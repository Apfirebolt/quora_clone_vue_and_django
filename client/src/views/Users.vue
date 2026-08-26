<template>
  <header-component />

  <main class="min-h-[calc(100vh-4rem)] bg-neutral/10 py-10 px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-6xl space-y-8">
      
      <!-- Top Section Header & Search Bar -->
      <div class="rounded-3xl border border-gray-100 bg-white p-6 sm:p-8 shadow-sm">
        <div class="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
          <SectionHeader
            title="Community Members"
            subtitle="Discover, connect, and collaborate with people across topics"
          />

          <!-- Integrated Search Input -->
          <div class="relative w-full sm:w-80">
            <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-gray-400">
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
            <input
              v-model="searchText"
              type="text"
              placeholder="Search members by username..."
              class="w-full rounded-xl border border-gray-200 bg-gray-50/60 py-2.5 pl-10 pr-4 text-sm text-gray-900 placeholder-gray-400 transition focus:border-primary focus:bg-white focus:outline-none focus:ring-2 focus:ring-primary/20"
            />
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <Loader v-if="isLoading" />

      <!-- Users Grid -->
      <div v-else-if="users && users.results && users.results.length > 0" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <article
          v-for="user in users.results"
          :key="user.id"
          class="group relative flex flex-col justify-between rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm transition-all duration-200 hover:-translate-y-1 hover:border-slate-300 hover:shadow-md"
        >
          <!-- User Profile Header & Metadata -->
          <div class="space-y-4">
            <div class="flex items-center gap-3.5">
              <!-- Avatar Initial Pill -->
              <div
                class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 text-base font-bold text-white shadow-sm ring-4 ring-blue-50"
              >
                {{ (user.username || 'U').charAt(0).toUpperCase() }}
              </div>

              <!-- Username & Handle -->
              <div class="min-w-0 flex-1">
                <h3 class="truncate text-base font-semibold text-slate-900 group-hover:text-primary transition-colors">
                  {{ user.username }}
                </h3>
                <p class="truncate text-xs text-slate-500">
                  {{ user.email || `@${user.username}` }}
                </p>
              </div>
            </div>

            <!-- Profile Info Chips -->
            <div class="flex items-center gap-2 pt-1">
              <span class="inline-flex items-center rounded-md bg-slate-50 px-2 py-1 text-xs font-medium text-slate-600 ring-1 ring-inset ring-slate-500/10">
                Contributor
              </span>
              <span class="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10">
                Member
              </span>
            </div>
          </div>

          <!-- Bottom Action -->
          <div class="mt-6 pt-4 border-t border-slate-100">
            <button
              @click="goToUserDetail(user)"
              class="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-slate-900 py-2.5 px-4 text-xs font-semibold text-white transition-all hover:bg-primary focus:outline-none focus:ring-2 focus:ring-primary/40 active:scale-[0.98]"
            >
              <span>View Profile</span>
              <span class="transition-transform group-hover:translate-x-0.5">→</span>
            </button>
          </div>
        </article>
      </div>

      <!-- Empty State -->
      <div
        v-else
        class="rounded-3xl border border-dashed border-slate-200 bg-white p-12 text-center"
      >
        <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-slate-100 text-slate-400">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <h3 class="mt-4 text-sm font-semibold text-slate-900">No members found</h3>
        <p class="mt-1 text-sm text-slate-500">
          {{ searchText ? `No users matching "${searchText}"` : "There are currently no registered members to display." }}
        </p>
      </div>

    </div>
  </main>

  <footer-component />
</template>

<script setup>
import { onMounted, computed, watch, ref } from "vue";
import { useUser } from "../store/user";
import { useRouter } from "vue-router";
import Loader from "../components/Loader.vue";
import SectionHeader from "../components/SectionHeader.vue";

const userStore = useUser();
const router = useRouter();
const searchText = ref("");
let timeoutId;

const debouncedSearch = (value) => {
  if (timeoutId) clearTimeout(timeoutId);
  timeoutId = setTimeout(() => {
    if (value && value.trim().length > 3) {
      userStore.getUsersAction(searchText.value.trim());
    } else {
      userStore.getUsersAction();
    }
  }, 400); // Optimized debounce to 400ms for snappier feedback
};

watch(searchText, debouncedSearch);

const users = computed(() => userStore.getUsers);
const isLoading = computed(() => userStore.isLoading);

const goToUserDetail = (user) => {
  router.push(`/users/${user.username}`);
};

onMounted(async () => {
  await userStore.getUsersAction();
});
</script>