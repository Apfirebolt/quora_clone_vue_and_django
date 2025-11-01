<template>
  <header-component />
  <main class="bg-white shadow sm:rounded-lg" id="about">
    <section class="px-4 py-5 sm:p-6 container mx-auto">
      <SectionHeader
        title="Users"
        subtitle="Browse and search for users on the platform"
      />
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
        <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <div
            v-for="user in users.results"
            :key="user.id"
            class="bg-gradient-to-br from-white to-gray-50 rounded-xl shadow-md hover:shadow-xl transition-all duration-300 border border-gray-100 overflow-hidden"
          >
            <div class="p-6">
              <div class="flex items-center space-x-4 mb-4">
                
                <div class="flex-1">
                  <h3 class="text-lg font-semibold text-gray-900 mb-1">
                    {{ user.username }}
                  </h3>
                  <p class="text-sm text-gray-600">
                    {{ user.email }}
                  </p>
                </div>
              </div>
              <div class="pt-4 border-t border-gray-100">
                <button
                  @click="goToUserDetail(user)"
                  class="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium py-2.5 px-4 rounded-lg transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  View Profile
                </button>
              </div>
            </div>
          </div>
        </div>
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
