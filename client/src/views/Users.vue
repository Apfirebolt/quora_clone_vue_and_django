<template>
  <header-component />
  <main class="bg-white shadow sm:rounded-lg" id="about">
    <section class="px-4 py-5 sm:p-6 container mx-auto">
      <SectionHeader title="Users" subtitle="Browse and search for users on the platform" />
      <Loader v-if="isLoading" />
      <div>
        <input
          v-model="searchText"
          @input="searchUsers"
          type="text"
          placeholder="Search users..."
          class="block rounded-md w-full border-primary shadow-sm focus:border-accent px-2 py-3 focus:ring-primary sm:text-sm"
        />
      </div>

      <div v-if="users && users.results" class="mt-5">
        <ul class="divide-y divide-gray-200">
          <li v-for="user in users.results" :key="user.id" class="py-4">
            <div class="flex space-x-3">
              <div class="flex-1 space-y-1">
                <p class="text-sm font-medium text-gray-900">
                  {{ user.email }}
                </p>
                <p class="text-sm text-gray-500">
                  {{ user.username }}
                </p>
              </div>
              <div>
                <button
                  @click="goToUserDetail(user)"
                  class="text-green-600 hover:text-green-900 mx-2 px-2 py-1 rounded-md shadow-lg"
                >
                  View
                </button>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </section>
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
    if (value.length > 3) {
      userStore.getUsersAction(searchText.value);
    } else {
      userStore.getUsersAction();
    }
  }, 1000); // Adjust delay as needed (in milliseconds)
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
